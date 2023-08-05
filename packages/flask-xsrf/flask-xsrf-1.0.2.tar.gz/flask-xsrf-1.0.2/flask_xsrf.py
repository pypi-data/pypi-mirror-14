"""
  flask-xsrf
  ~~~~~~~~~~

  flask extension for defending against cross-site request forgery attacks
  (XSRF/CSRF).

  :usage:

    from flask import Flask, Response, session
    from flask.ext import xsrf

    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'session_secret_key'
    app.config['session_cookie_secure'] = True

    @app.before_request
    def before_request():
      if 'user_id' not in session:
        session['user_id'] = 'random_generated_anonymous_id'

    def get_user_id():
      return session.get('user_id')

    xsrfh = xsrf.XSRFTokenHandler(
      user_func=get_user_id, secret='xsrf_secret', timeout=3600)

    @app.route('/create', methods=['GET'])
    @xsrfh.send_token()
    def create_get():
      return Response('success')

    @app.route('/create', methods=['POST'])
    @xsrfh.handle_token()
    def create_post():
      return Response('success')


  :author: @gregorynicholas
  :license: MIT, see LICENSE for more details.
"""
import hmac
import time
import base64
import hashlib
from flask import request
from flask import session
from functools import wraps
from werkzeug import exceptions

__all__ = ['XSRFTokenHandler', 'XSRFToken', 'XSRFTokenUserIdInvalid',
'XSRFTokenMalformed', 'XSRFTokenExpiredException', 'XSRFTokenInvalid',
'TOKEN_FORM_NAME', 'TOKEN_HEADER_NAME']


class XSRFException(exceptions.HTTPException):
  pass

class XSRFTokenMalformed(XSRFException, exceptions.NotAcceptable):
  pass

class XSRFTokenExpiredException(XSRFException, exceptions.Unauthorized):
  pass

class XSRFTokenInvalid(XSRFException, exceptions.NotAcceptable):
  pass

class XSRFTokenUserIdInvalid(XSRFException, exceptions.NotAcceptable):
  pass

TOKEN_FORM_NAME = 'xsrf-token'
TOKEN_HEADER_NAME = 'X-XSRF-Token'


class XSRFTokenHandler:
  def __init__(self, user_func, secret, timeout=10):
    '''
      :param user_func: Function which returns an key string for the current user.
      :param secret: String secret.
      :param timeout: Integer for the number of seconds the token is active for.
    '''
    self.user_func = user_func
    self.secret = secret
    self.timeout = timeout

  def send_token(self):
    def wrapper(func):
      @wraps(func)
      def decorated(*args, **kw):
        user_id = self.user_func()
        if not user_id:
          raise XSRFTokenUserIdInvalid('XSRFTokenUserIdInvalid')
        self.token = XSRFToken(user_id=user_id, secret=self.secret)
        session[TOKEN_FORM_NAME] = self.token.generate_token_string()
        response = func(*args, **kw)
        response.headers.add(TOKEN_HEADER_NAME, session[TOKEN_FORM_NAME])
        return response
      return decorated
    return wrapper

  def handle_token(self):
    def wrapper(func):
      @wraps(func)
      def decorated(*args, **kw):
        user_id = self.user_func()
        if not user_id:
          raise XSRFTokenUserIdInvalid('UserId not valid.')
        self.token = XSRFToken(user_id=user_id, secret=self.secret)
        # parse the token string..
        request_token_string = self.parse_xsrftoken_from_request()
        token_string = session.pop(TOKEN_FORM_NAME, None)
        # validate the token string..
        self.verify_token(token_string, request_token_string)
        return func(*args, **kw)
      return decorated
    return wrapper

  def verify_token(self, token_string, request_token_string):
    if not token_string:
      raise XSRFTokenInvalid('Token not set.')
    if not request_token_string:
      raise XSRFTokenInvalid('Request token not valid.')
    if token_string != request_token_string:
      raise XSRFTokenInvalid('Token not valid.')
    self.token.verify_token_string(token_string, timeout=self.timeout)

  def parse_xsrftoken_from_request(self):
    # get the value from a request header..
    value = request.headers.get(TOKEN_HEADER_NAME)
    if value is None or len(value) < 1:
      # get the value from form params..
      value = request.form.get(TOKEN_FORM_NAME)
    return value


class XSRFToken(object):
  _DELIMITER = '|'

  def __init__(self, user_id, secret, current_time=None):
    """Initializes the XSRFToken object.

    :param user_id:
      A string representing the user that the token will be valid for.
    :param secret:
      A string containing a secret key that will be used to seed the
      hash used by the :class:`XSRFToken`.
    :param current_time:
      An int representing the number of seconds since the epoch. Will be
      used by `verify_token_string` to check for token expiry. If `None`
      then the current time will be used.
    """
    self.user_id = user_id
    self.secret = secret
    if current_time is None:
      self.current_time = int(time.time())
    else:
      self.current_time = int(current_time)

  def _digest_maker(self):
    return hmac.new(self.secret, digestmod=hashlib.sha256)

  def generate_token_string(self, action=None):
    """Generate a hash of the given token contents that can be verified.

    :param action:
      A string representing the action that the generated hash is valid
      for. This string is usually a URL.
    :returns:
      A string containing the hash contents of the given `action` and the
      contents of the `XSRFToken`. Can be verified with
      `verify_token_string`. The string is base64 encoded so it is safe
      to use in HTML forms without escaping.
    """
    digest_maker = self._digest_maker()
    digest_maker.update(self.user_id)
    digest_maker.update(self._DELIMITER)
    if action:
      digest_maker.update(action)
      digest_maker.update(self._DELIMITER)

    digest_maker.update(str(self.current_time))
    return base64.urlsafe_b64encode(
      self._DELIMITER.join(
        [digest_maker.hexdigest(),
        str(self.current_time)]
      ))

  def verify_token_string(self, token_string, action=None, timeout=None,
    current_time=None):
    """Generate a hash of the given token contents that can be verified.

    :param token_string:
      A string containing the hashed token (generated by
      `generate_token_string`).
    :param action:
      A string containing the action that is being verified.
    :param timeout:
      An int or float representing the number of seconds that the token
      is valid for. If None then tokens are valid forever.
    :current_time:
      An int representing the number of seconds since the epoch. Will be
      used by to check for token expiry if `timeout` is set. If `None`
      then the current time will be used.
    :raises:
      XSRFTokenMalformed if the given token_string cannot be parsed.
      XSRFTokenExpiredException if the given token string is expired.
      XSRFTokenInvalid if the given token string does not match the
      contents of the `XSRFToken`.
    """
    try:
      decoded_token_string = base64.urlsafe_b64decode(token_string)
    except TypeError:
      raise XSRFTokenMalformed()

    split_token = decoded_token_string.split(self._DELIMITER)
    if len(split_token) != 2:
      raise XSRFTokenMalformed()

    try:
      token_time = int(split_token[1])
    except ValueError:
      raise XSRFTokenMalformed()

    if timeout is not None:
      if current_time is None:
        current_time = time.time()
      # If an attacker modifies the plain text time then it will not match
      # the hashed time so this check is sufficient.
      if (token_time + timeout) < current_time:
        raise XSRFTokenExpiredException()

    expected_token = XSRFToken(self.user_id, self.secret, token_time)
    expected_token_string = expected_token.generate_token_string(action)

    if len(expected_token_string) != len(token_string):
      raise XSRFTokenInvalid()

    # Compare the two strings in constant time to prevent timing attacks.
    different = 0
    for a, b in zip(token_string, expected_token_string):
      different |= ord(a) ^ ord(b)
    if different:
      raise XSRFTokenInvalid()
