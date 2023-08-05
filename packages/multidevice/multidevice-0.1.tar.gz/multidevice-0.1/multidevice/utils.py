from __future__ import absolute_import

# global imports
import pytz
import datetime
import hashlib
import hmac
import base64

# django level imports
from django.conf import settings
from django.utils.importlib import import_module


tz = settings.TIME_ZONE


def get_current_time():
    """
    Utility method for returning current date time
    with time zone

    :retruns: Current datetime object
    """
    return pytz.timezone(tz).localize(datetime.datetime.now())


def get_application_session_id(application, token):
    """
    Utility method to generate unique session id signed by user token

    :params application: Application Name
    :params token: User token
    """
    session_id = base64.b64encode(hmac.new(
        str(token), application, hashlib.sha256).digest())
    return session_id


def get_registered_callback(callback_function):
    """
    Callback method import

    :params callback_function: string path of module
    :returns: function
    """
    callback = None
    try:
        mod, callback = callback_function.rsplit('.', 1)
        module = import_module(mod)
        callback = getattr(module, callback)
    except Exception, e:
        pass
    return callback


def delete_session(session_key):
    """
    Method to delete user session based on session key

    :params session_key: session object key
    """
    # delete session of currently logged in user as same user is
    # logged in somewhere else
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)
    session.delete()
