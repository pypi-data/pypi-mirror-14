from django.utils.translation import ugettext_lazy as _


CLIENT_CONFIDENTIAL = 'confidential'
CLIENT_PUBLIC = 'public'
CLIENT_TYPES = (
    (CLIENT_CONFIDENTIAL, _('Confidential')),
    (CLIENT_PUBLIC, _('Public')),
)

GRANT_AUTHORIZATION_CODE = 'authorization-code'
GRANT_IMPLICIT = 'implicit'
GRANT_PASSWORD = 'password'
GRANT_CLIENT_CREDENTIALS = 'client-credentials'
GRANT_TYPES = (
    (GRANT_AUTHORIZATION_CODE, _('Authorization code')),
    (GRANT_IMPLICIT, _('Implicit')),
    (GRANT_PASSWORD, _('Resource owner password-based')),
    (GRANT_CLIENT_CREDENTIALS, _('Client credentials')),
)

GRANT_TYPE_MAPPING = {
    'authorization_code': (
        GRANT_AUTHORIZATION_CODE,
    ),
    'password': (
        GRANT_PASSWORD,
    ),
    'client_credentials': (
        GRANT_CLIENT_CREDENTIALS,
    ),
    'refresh_token': (
        GRANT_AUTHORIZATION_CODE,
        GRANT_PASSWORD,
        GRANT_CLIENT_CREDENTIALS,
    )
}
