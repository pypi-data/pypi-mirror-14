from __future__ import absolute_import

from django.conf import settings

from disable_multidevice_login.utils import get_registered_callback

VALID_API_VERSION = settings.MULTI_DEVICE_API_VERSION
APPLICATION_NAME = settings.APPLICATION_NAME

# User check callback
try:
    exclude_user_check = settings.USER_CHECK_CALLBACK
except AttributeError, e:
    exclude_user_check = None
else:
    exclude_user_check = get_registered_callback(exclude_user_check)


# Flag to enable/disable session expiry of inactive session
DEFAULT_INACTIVE_SESSION_TIMEOUT = 60 * 60

EXPIRE_INACTIVE_SESSION = getattr(settings, "EXPIRE_INACTIVE_SESSION", False)

INACTIVE_SESSION_TIMEOUT = getattr(
    settings, "INACTIVE_SESSION_TIMEOUT",
    DEFAULT_INACTIVE_SESSION_TIMEOUT)
