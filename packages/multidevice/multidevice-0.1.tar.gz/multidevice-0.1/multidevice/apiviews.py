from __future__ import absolute_import

# django imports
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import parsers, renderers
from rest_framework import authentication

# disable_multidevice_login imports
from disable_multidevice_login.error_codes import ERROR_CODES
from disable_multidevice_login.utils import get_application_session_id
from disable_multidevice_login.login_manager import UserLoginState
from disable_multidevice_login.signals import clear_device_login
from disable_multidevice_login.login_manager import DeviceLoginManagerClass
from disable_multidevice_login.exceptions import MultiLogginFound
from disable_multidevice_login.exceptions import InactiveSessionFound
from disable_multidevice_login.utils import delete_session


class AppLoginAPIView(APIView):
    """
    API View for fetching user token and registring user's
    login state in specific application
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser,
        parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        API endpoint with method post

        :params request: HTTP Request instance

        :returns: HTTP API response
        """
        errors = []
        data = dict()
        success = True
        status_code = status.HTTP_200_OK
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Application ID required to build session key
        try:
            # get application name from request headers
            application_id = request.META["HTTP_APPLICATION"]
            token_key = token.key
            session_key = get_application_session_id(
                application_id, token_key)
            custom_session = True

            # Logic for checking user logged in state
            login_state = UserLoginState(
                user, session_key, application=application_id,
                custom_session=custom_session)
            login_state.manage_device_login(request)
        except (MultiLogginFound, InactiveSessionFound), e:
            if isinstance(e, InactiveSessionFound):
                delete_session(e.session_key)
                device_manager = DeviceLoginManagerClass()
                device_manager.invalidate_user_login_details(user)

            # case if user is found logged in with multiple devices
            # or user session is inactive
            success = False
            errors = [{
                "error_code": e.error_code,
                "error_message": e.message}]
            status_code = status.HTTP_403_FORBIDDEN
        except KeyError, e:
            success = False
            errors = [{
                "error_code": "Login:101",
                "error_message": ERROR_CODES["Login:101"]}]
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            data = {"token": token.key, "session_key": session_key}
        response = {"data": data, "errors": errors, "success": success}
        return Response(response, status_code)


class AppLogoutAPIView(APIView):
    """
    API View for logging out from application
    session can be managed at application level but
    as soon as logout is performed application is bound to
    send API call to register user login state in backend
    """
    authentication_classes = (
        authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        """
        API endpoint to update user login state

        :params request: HTTP Request instance

        :returns: HTTP API Response
        """
        user = request.user
        auth_logout(request)
        clear_device_login(user.__class__, user, request)
        response = {
            "success": True, "errors": [],
            "message": "User %s is successfully logged out!" % user.username}
        return Response(response, status=status.HTTP_200_OK)
