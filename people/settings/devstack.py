from people.settings.local import *

# Generic OAuth2 variables irrespective of SSO/backend service key types.
OAUTH2_PROVIDER_URL = 'http://edx.devstack.lms:18000/oauth2'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'people',
        'LOCATION': [
            'people.memcache'
        ]
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'people',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'people.db',
        'PORT': '3306',
    }
}

# OAuth2 variables specific to social-auth/SSO login use case.
SOCIAL_AUTH_EDX_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_KEY', 'people-sso-key')
SOCIAL_AUTH_EDX_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_SECRET', 'people-sso-secret')
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_ISSUER', 'http://localhost:18000')
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT', 'http://edx.devstack.lms:18000')
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL', 'http://localhost:18000/logout')
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = os.environ.get(
    'SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT', 'http://localhost:18000',
)

# OAuth2 variables specific to backend service API calls.
BACKEND_SERVICE_EDX_OAUTH2_KEY = os.environ.get('BACKEND_SERVICE_EDX_OAUTH2_KEY', 'people-backend-service-key')
BACKEND_SERVICE_EDX_OAUTH2_SECRET = os.environ.get('BACKEND_SERVICE_EDX_OAUTH2_SECRET', 'people-backend-service-secret')

JWT_AUTH.update({
    'JWT_SECRET_KEY': SOCIAL_AUTH_EDX_OAUTH2_SECRET,
    'JWT_ISSUER': 'http://localhost:18000/oauth2',
    'JWT_AUDIENCE': SOCIAL_AUTH_EDX_OAUTH2_KEY,
})
