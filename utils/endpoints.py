

#################################
#          CALL CENTER          #
#################################
CALL_CENTER = '/call_center'
PRESET_QUERY_SERVICE = '/preset/query'
SKILLS = '/skills'
AGENTS = '/agents'


#################################
#             USERS             #
#################################
USER = '/user'
USERS = '/users'

USERS_PASSWORD = '/users/password'          # change user password

LOGOUT = '/users/logout'              # always 200
USER_ID_LOGOUT = '/users/{id}/logout' # if logged out already => 400

#################################
#             AUTH              #
#################################
SIGNUP = '/signup'
USERINFO = '/userinfo'

LOGIN = '/login'
LOGIN_2FA = '/login/2fa'

#################################
#           SETTINGS            #
#################################
SETTINGS = '/settings'
SETTINGS_AVAILABLE = '/settings/available'

#################################
#            DEVICES            #
#################################
DEVICES = '/devices'
DEVICES_ID_REGISTERED = '/devices/{id}/registered' #{device.id}  NOT IMPLEMENTED
DEVICES_ID_USERS_AUDIT = '/devices/{id}/users/audit'