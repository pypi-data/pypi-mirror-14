"""
************************
SpaceTrackAPI.urlbuilder
************************

This module contains functions building the urls for the Space-Track API
"""


import urllib.parse


BASE_URL = 'https://www.space-track.org'
_authentication_url = {
    'login': '/ajaxauth/login',
    'logout': '/ajaxauth/logout'
}
_controllers_list = (
    'basicspacedata',
    'expandedspacedata',
    'fileshare'
)
_actions_list = (
    'query',
    'modeldef'
)


def login():
    """Returns the login url

    Return:
        str: Login url
    """

    return BASE_URL + _authentication_url['login']

def logout():
    """Returns the logout url

    Return:
        str: Logout url
    """

    return BASE_URL + _authentication_url['logout']

def build(controller, action, request_class, predicates = {}):
    """Builds an url for the API

    Args:
        controller (str): Request controller.
        action (str): Request action.
        request_class (str): Request class
        predicates (Optional[dict]): List of predicates

    Returns:
        str: url

    Raises:
        ValueError: Incorrect parameter
    """

    # Check if the parameters are correct
    if controller not in _controllers_list:
        raise ValueError('Incorrect parameter "controller" : ' + controller)
    if action not in _actions_list:
        raise ValueError('Incorrect parameter "action" : ' + action)

    # Builing the url
    url = '/' + urllib.parse.quote(controller) + '/' + action
    url += '/class/' + urllib.parse.quote(request_class)

    for key, value in predicates.items():
        url += '/' + urllib.parse.quote(str(key))
        url += '/' + urllib.parse.quote(str(value))

    return BASE_URL + url
