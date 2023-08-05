from __future__ import absolute_import

from disable_multidevice_login.login_manager import DeviceLoginManagerClass


def clear_device_login(sender, user, request, **kwargs):
    """
    Signal utility method to handle user logout. It will be called
    as soon user logout from system

    :params sender: Sender as User model
    :params user: User model object
    :params request: Request Instance
    """
    if user:
        device_mgr = DeviceLoginManagerClass()
        return device_mgr.invalidate_user_login_details(user)
    return False
