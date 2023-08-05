from __future__ import absolute_import

# rest framework imports
from rest_framework import permissions
from rest_framework import status

# multi device login imports
from disable_multidevice_login.login_manager import UserLoginState
from disable_multidevice_login.exceptions import MultiLogginFound
from disable_multidevice_login.exceptions import InactiveSessionFound


class DeviceLoginPermission(permissions.IsAuthenticated):
    """
    Permission class to handle incomming requests and tracking request timeout
    in case inactivity of session.
    """
    def has_permission(self, request, view):
        """
        Method which is invoked from api interface to handle
        device session

        :args request: Request instance
        :args view: API View
        :returns: True/False
        """
        access = super(DevicePermission, self).has_permission(request, view)
        if access:
            try:
                user = request.user
                # get application name from request headers
                application_session = request.META.get("HTTP_DEVICE_SESSION")
                if application_session:
                    # user session key to maintain login info
                    session_key = request.session.session_key
                    login_state = UserLoginState(
                        user, session_key, application=self.application)
                    login_state.manage_device_login(request)
                else:
                    access = True
            except (MultiLogginFound, InactiveSessionFound), e:
                access = False
                self.message = e.message
        return access
