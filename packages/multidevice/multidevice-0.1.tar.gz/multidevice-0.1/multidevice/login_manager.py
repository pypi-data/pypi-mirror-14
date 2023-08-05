from __future__ import absolute_import

try:
    import pickle
except ImportError, e:
    import cPickle as pickle

# django imports
from django.conf import settings
from django.core.cache import caches
from importlib import import_module

# app level imports
from disable_multidevice_login.exceptions import MultiLogginFound
from disable_multidevice_login.exceptions import InactiveSessionFound
from disable_multidevice_login.utils import get_current_time
from disable_multidevice_login.error_codes import ERROR_CODES
from disable_multidevice_login import exclude_user_check
from disable_multidevice_login import EXPIRE_INACTIVE_SESSION
from disable_multidevice_login import INACTIVE_SESSION_TIMEOUT
from disable_multidevice_login.error_codes import ERROR_CODES


class UserDeviceLogginInfoContainer(object):
    """
    Container class which contains information of
    login User.
    """
    user = None
    device_logged_in = False
    session_key = None
    last_logged_in = None
    application = None
    custom_session = False

    def set_details(
            self, request, session_key, device_logged_in=True,
            application=None, custom_session=False):
        """
        Set login details from request

        :params request: Request instance to extract user information
        :params device_logged_in: Flag which maintain user logged in state
        """
        self.user = request.user
        self.device_logged_in = device_logged_in
        self.session_key = session_key
        self.agent = request.META.get("HTTP_USER_AGENT", None)
        self.client_ip = request.META.get("REMOTE_HOST", None)
        self.last_logged_in = get_current_time()
        self.custom_session = custom_session
        self.application = request.GET.get(
            "application", None) or application
        return True


class DeviceLoginManagerClass(object):
    """
    Manager class for managing user login information
    """
    cache_timeout = settings.SESSION_COOKIE_AGE
    cache = caches['default']

    def get_cache_key(self, user):
        """
        Common helper method to build key of user

        :params user: User instance
        :returns: cache key
        """
        cache_key = "user_%s_loggin_info" % user.pk
        return cache_key

    def get_cache_details(self, user):
        """
        Common helper method to return cache details
        against key

        :params user: user object
        :returns: user logged in details
        """
        cache_key = self.get_cache_key(user)
        user_info = self.cache.get(cache_key)
        info = pickle.loads(user_info) if user_info else None
        return info

    def set_cache_details(self, user, login_info):
        """
        Common helper method to set cache details
        against key

        :params user: user object
        :params login_info: user logged in details

        :returns: True/False
        """
        cache_key = self.get_cache_key(user)
        cache_data = pickle.dumps(login_info)
        return self.cache.set(
            cache_key, cache_data,
            timeout=self.cache_timeout)

    def invalidate_user_login_details(self, user):
        """
        Common helper method to invalidate cache details
        and loggedin information for user.
        Mainly being called as soon as user is logged out

        :params user: User object

        :returns: deleted status of cache key 0/1
        """
        cache_key = self.get_cache_key(user)
        return self.cache.delete(cache_key)


class UserLoginState(object):
    """
    Class to manage user login state, Being used in API
    middleware
    """
    device_manager = DeviceLoginManagerClass()

    def __init__(
            self, user, session_key, application=None,
            custom_session=False):
        """
        Initializing utility to manage user login

        :params user: User object
        :params session_key: Session Key
        :params application: Application name from where user is logged in
        :params custom_session: flag true/false based on session managed
         by django or some other application
        """
        self.user = user
        self.session_key = session_key
        self.application = application
        self.custom_session = custom_session

    def check_inactive_session(self, user_info):
        """
        Inactive session expiration in case user had not accessed
        system since configured INACTIVE_SESSION_TIMEOUT

        :params user_info: user login details object

        :raises: InactiveSessionFound error in case user session is
         inactive since SESSION_TIMEOUT_LIMIT

        :returns: False if no need to expire user session
        """
        last_login = user_info.last_logged_in
        current_time = get_current_time()
        last_updated = (current_time - last_login).seconds
        if last_updated >= INACTIVE_SESSION_TIMEOUT:
            error_code = "Login:102"
            message = ERROR_CODES[error_code]
            raise InactiveSessionFound(
                error_code, message, session_key=user_info.session_key)
        self.update_login_details(user_info)
        return False

    def check_active_session(self, old_session_key, custom_session=False):
        """
        Checks for session active state. allows user login if user past
        session is got inactive.
        also if session is inactive deletes the login details and creates
        new session details

        :params old_session_key: already stored session key
        :params custom_session: flag is login details had been set by django

        :returns: bool flag True/False
        """
        allow = False
        if not custom_session:
            engine = import_module(settings.SESSION_ENGINE)
            SessionStore = engine.SessionStore
            session = SessionStore(old_session_key)
            if not session._session:
                allow = True
        return allow

    def update_login_details(self, user_info):
        """
        update cache of login details for user

        :params request: request instance
        """
        last_login = user_info.last_logged_in
        current_time = get_current_time()
        last_updated = (current_time - last_login).seconds
        # update login details every 60 sec.
        if last_updated >= 60:
            user_info.last_logged_in = current_time
            self.device_manager.set_cache_details(self.user, user_info)
        return True

    def set_login_details(self, request):
        """
        Create cache of login details for user

        :params request: request instance
        """
        # No multilogin found
        user_info = UserDeviceLogginInfoContainer()
        user_info.set_details(
            request, self.session_key, device_logged_in=True,
            application=self.application,
            custom_session=self.custom_session)
        self.device_manager.set_cache_details(self.user, user_info)

    def already_loggedin(self, user_info):
        """
        Checked if user session is same and already loggedin somewhere
        in other device

        :params user_info: user login details object
        :raises: MultiLogginFound in case user is loggedin in other device

        :returns: False
        """
        same_session = (self.session_key == user_info.session_key)

        if user_info.device_logged_in and not same_session:
            error_code = "Login:100"
            application = user_info.application
            device = user_info.agent
            message = ERROR_CODES[error_code].format(user=self.user.username)
            raise MultiLogginFound(
                error_code, message,
                session_key=user_info.session_key,
                device=device,
                application=application)
        return False

    def manage_device_login(self, request):
        """
        Common method to which manages user's login state across multiple
        endpoints

        :params request: request instance
        :raises: MultiLogginFound, InactiveSessionFound
        """
        exclude_current_user = False
        try:
            if exclude_user_check and callable(exclude_user_check):
                exclude_current_user = exclude_user_check(self.user)
        except Exception, e:
            exclude_current_user = False

        if not exclude_current_user:
            user_info = self.device_manager.get_cache_details(self.user)
            if user_info:
                allow = self.check_active_session(
                    user_info.session_key,
                    custom_session=user_info.custom_session)

                # allow user login if session is inactive but device
                # login flag is set here it will reset the device
                # login data
                if allow:
                    self.set_login_details(request)
                    user_info = self.device_manager.get_cache_details(
                        self.user)
                self.check_inactive_session(user_info)
                self.already_loggedin(user_info)
            else:
                self.set_login_details(request)
