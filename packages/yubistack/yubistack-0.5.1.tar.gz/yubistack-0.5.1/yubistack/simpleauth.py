"""

yubistack.simpleauth
~~~~~~~~~~~~~~~~~~~~

Yubistack - Simple integrated auth
"""

from datetime import datetime
import logging
import time

from passlib.context import CryptContext

from .config import (
    settings,
    TS_SEC,
    TS_REL_TOLERANCE,
    TS_ABS_TOLERANCE,
    TOKEN_LEN,
)
from .db import DBHandler
from .utils import (
    decrypt_otp,
    counters_gte,
)

logger = logging.getLogger(__name__)

class AuthFail(Exception):
    """ Exception raised in case of authentication failures """
    pass


class DBH(DBHandler):
    """
    Extending the generic DBHandler class with the required queries
    """
    def get_user(self, username):
        """
        Read user information for Yubiauth
        """
        query = """SELECT users.attribute_association_id AS users_attribute_association_id,
                          users.id AS users_id, users.name AS users_name,
                          users.auth AS users_auth
                     FROM users
                    WHERE users.name = %s"""
        self._execute(query, (username,))
        return self._dictfetchone()

    def get_token(self, user_id, token_id):
        """
        Read user attribute information for Yubiauth
        """
        query = """SELECT yubikeys.attribute_association_id AS yubikeys_attribute_association_id,
                          yubikeys.id AS yubikeys_id,
                          yubikeys.prefix AS yubikeys_prefix,
                          yubikeys.enabled AS yubikeys_enabled
                     FROM yubikeys
               INNER JOIN user_yubikeys
                       ON user_yubikeys.yubikey_id = yubikeys.id
                    WHERE user_yubikeys.user_id = %s
                      AND yubikeys.prefix = %s"""
        self._execute(query, (user_id, token_id))
        return self._dictfetchone()

    def get_local_params(self, yk_publicname):
        """ Get yubikey parameters from DB """
        query = """SELECT active,
                          modified,
                          yk_publicname,
                          yk_counter,
                          yk_use,
                          yk_low,
                          yk_high,
                          nonce
                     FROM yubikeys
                    WHERE yk_publicname = %s"""
        self._execute(query, (yk_publicname,))
        local_params = self._dictfetchone()
        if not local_params:
            local_params = {
                'active': 1,
                'modified': -1,
                'yk_publicname': yk_publicname,
                'yk_counter': -1,
                'yk_use': -1,
                'yk_low': -1,
                'yk_high': -1,
                'nonce': '0000000000000000',
                'created': int(time.time())
            }
            # Key was missing in DB, adding it
            self.add_new_identity(local_params)
            logger.warning('Discovered new identity %s', yk_publicname)
        logger.debug('Auth data: %s', local_params)
        return local_params

    def add_new_identity(self, identity):
        """ Create new key identity """
        query = """INSERT INTO yubikeys (
                       active,
                       created,
                       modified,
                       yk_publicname,
                       yk_counter,
                       yk_use,
                       yk_low,
                       yk_high,
                       nonce
                ) VALUES (
                       %(active)s,
                       %(created)s,
                       %(modified)s,
                       %(yk_publicname)s,
                       %(yk_counter)s,
                       %(yk_use)s,
                       %(yk_low)s,
                       %(yk_high)s,
                       %(nonce)s
                )"""
        try:
            self._execute(query, identity)
            self._db.commit()
        except Exception as err:
            self._db.rollback()
            logger.exception('DB Error: %s', err)
            raise

    def update_db_counters(self, params):
        """ Update table with new counter values """
        query = """UPDATE yubikeys
                      SET modified = %(modified)s,
                          yk_counter = %(yk_counter)s,
                          yk_use = %(yk_use)s,
                          yk_low = %(yk_low)s,
                          yk_high = %(yk_high)s,
                          nonce = %(nonce)s
                    WHERE yk_publicname = %(yk_publicname)s
                      AND (yk_counter < %(yk_counter)s
                       OR (yk_counter = %(yk_counter)s
                      AND yk_use < %(yk_use)s))"""
        try:
            self._execute(query, params)
            self._db.commit()
        except Exception as err:
            self._db.rollback()
            logger.exception('DB Error: %s', err)
            raise


class SimpleClient:
    """ Authentication Client """
    def __init__(self):
        self.authdb = DBH(db='yubiauth')
        self.valdb = DBH(db='ykval')
        self.pwd_context = CryptContext(**settings['CRYPT_CONTEXT'])
        if settings['USE_NATIVE_YKKSM']:
            from .ykksm import Decryptor
            self.decryptor = Decryptor()
        else:
            self.decryptor = None

    def _get_user_info(self, username):
        """
        Get user from DB

        Args:
            username

        Returns:
            dictionary of user data

        Raises:
            AuthFail if user does not exist
        """
        user = self.authdb.get_user(username)
        if not user:
            raise AuthFail("No such user: %s" % username)
        logger.debug('Found user: %s', user)
        return user

    def _check_token(self, user, token_id):
        """
        Check Token association with user

        Args:
            user: User data dict as recieved from _get_user_info()
            token_id: Token prefix (aka. publicname)

        Returns:
            None

        Raises:
            AuthFail if token is not associated with the user
            AithFail if token is disabled
        """
        token = self.authdb.get_token(user['users_id'], token_id)
        if not token:
            logger.error('Token %s is not associated with %s', token_id, user['users_name'])
            raise AuthFail('Token %s is not associated with %s' % (token_id, user['users_name']))
        logger.debug('Found token: %s', token)
        if not token.get('yubikeys_enabled'):
            logger.error('Token %s is disabled for %s', token_id, user['users_name'])
            raise AuthFail('Token is disabled for %s' % user['users_name'])

    def _validate_password(self, user, password):
        """
        Validate password against the hash in SQL
        """
        valid, new_hash = self.pwd_context.verify_and_update(str(password), user['users_auth'])
        if not valid:
            logger.error('Invalid password for %(users_name)s', user)
            raise AuthFail('Invalid password for %(users_name)s' % user)
        if new_hash:
            # TODO: update user's hash with new_hash
            logger.warning("User %(users_name)s's hash needs update", user)
        return True

    def _decode_otp(self, otp):
        """ Decode OTP from input """
        otp_info = decrypt_otp(otp, urls=settings['YKKSM_SERVERS'],
                               decryptor=self.decryptor)
        if not otp_info:
            raise AuthFail("BAD_OTP: Can't decrypt OTP")
        logger.debug('Decrypted OTP: %s', otp_info)
        return otp_info

    def _build_otp_params(self, otp, otp_info):
        """ Build OTP params """
        return {
            'modified': int(time.time()),
            'otp': otp,
            'nonce': '0000000000000000',
            'yk_publicname': otp[:-TOKEN_LEN],
            'yk_counter': otp_info['counter'],
            'yk_use': otp_info['use'],
            'yk_high': otp_info['high'],
            'yk_low': otp_info['low'],
        }

    def _validate_otp(self, otp_params, local_params):
        """ Validate OTP """
        # Check the OTP counters against local DB
        if counters_gte(local_params, otp_params):
            logger.warning('Replayed OTP: Local counters higher (%s > %s)',
                           local_params, otp_params)
            raise AuthFail('REPLAYED_REQUEST: OTP was already used')
        # Valid OTP, update DB
        self.valdb.update_db_counters(otp_params)

    def _phishing_test(self, otp_params, local_params):
        """ Run a timing phishing test """
        # We only need phishing test if the Yubikey was not re-inserted
        if otp_params['yk_counter'] != local_params['yk_counter']:
            return
        new_ts = (otp_params['yk_high'] << 16) + otp_params['yk_low']
        old_ts = (local_params['yk_high'] << 16) + local_params['yk_low']
        ts_delta = (new_ts - old_ts) * TS_SEC

        # Check real time
        last_time = local_params['modified']
        now = int(time.time())
        elapsed = now - last_time
        deviation = abs(elapsed - ts_delta)

        # Time delta server might verify multiple OTPS in a row. In such case validation server
        # doesn't have time to tick a whole second and we need to avoid division by zero.
        if elapsed:
            percent = deviation / elapsed
        else:
            percent = 1
        if deviation > TS_ABS_TOLERANCE and percent > TS_REL_TOLERANCE:
            logger.error('%s: OTP Expired:\n\tTOKEN TS OLD: %s\n\t'
                         'TOKEN TS NOW: %s\n\tTOKEN TS DIFF: %s (sec)\n\t'
                         'ACCESS TS OLD: %s\n\tACCESS TS NEW: %s\n\t'
                         'ACCESS TS DIFF: %s (sec)\n\tDEVIATION: %s (sec) or %s%%',
                         otp_params['otp'][:-TOKEN_LEN],
                         datetime.utcfromtimestamp(old_ts),
                         datetime.utcfromtimestamp(new_ts),
                         ts_delta,
                         datetime.utcfromtimestamp(last_time),
                         datetime.utcfromtimestamp(now),
                         elapsed,
                         deviation, percent)
            raise AuthFail('DELAYED_OTP: OTP expired')

    def _verify_otp(self, otp):
        """
        Verify OTP

        Verification steps:
            1. Decrypt OTP
            2. Compare counters
            3. Phishing test (comparing timers)
        """
        # STEP 1: Decrypt OTP
        otp_info = self._decode_otp(otp)
        # STEP 2: Compare counters
        local_params = self.valdb.get_local_params(otp[:-TOKEN_LEN])
        if not local_params['active']:
            logger.error('De-activated Yubikey: %(yk_publicname)s', local_params)
            raise AuthFail('BAD_OTP: Yubikey %s is disabled' % otp[:-TOKEN_LEN])
        otp_params = self._build_otp_params(otp, otp_info)
        self._validate_otp(otp_params, local_params)
        # STEP 3: Phishing test (comparing timers)
        self._phishing_test(otp_params, local_params)

    def authenticate(self, username, password, otp):
        """
        Integrated user authentication

        Args:
            username: Username of the user?!
            password: Password of the user?!
            otp: Yubikey one time password

        Returns:
            dict of authentication data

        1. Check if token is enabled
        2. Check if token is associated with the user
        3. Validate users password
        4. Validate OTP (YKVal)
        """
        auth_start = time.time()
        try:
            user = self._get_user_info(username)
            self._check_token(user, otp[:-TOKEN_LEN])
            self._validate_password(user, password)
            self._verify_otp(otp)
        except AuthFail as err:
            logger.info('%s: Failed authentication: %s', username, err)
            return {'status_code': 400, 'username': username,
                    'token_id': otp[:-TOKEN_LEN],
                    'message': str(err),
                    'latency': round(time.time() - auth_start, 3)}
        except Exception as err:
            logger.exception('%s: Backend error: %s', username, err)
            return {'status_code': 500, 'username': username,
                    'token_id': otp[:-TOKEN_LEN],
                    'message': 'backend error: %s' % err,
                    'latency': round(time.time() - auth_start, 3)}
        logger.info('%s: Successful authentication', username)
        return {'status_code': 200, 'username': username,
                'token_id': otp[:-TOKEN_LEN],
                'message': 'Successfully authenticated',
                'latency': round(time.time() - auth_start, 3)}

