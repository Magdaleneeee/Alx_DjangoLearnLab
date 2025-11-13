"""
Django settings for LibraryProject project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

# ❗ In production this must be False, but for ALX tasks we keep it False
DEBUG = False

# Allow all hosts (only for learning projects)
ALLOWED_HOSTS = ['*']


# ---------------------------
#   INSTALLED APPS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'bookshelf',
    'relationship_app',
    'accounts',
]

# ---------------------------
#   MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# ---------------------------
#   DATABASE
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------------------
#   PASSWORD VALIDATION
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------
#   INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------
#   SECURITY SETTINGS (TASK 3)
# ---------------------------

# 🔒 Forces all traffic to HTTPS
SECURE_SSL_REDIRECT = True

# 🔒 Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 🔒 Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# 🔒 Browser-level XSS protection
SECURE_BROWSER_XSS_FILTER = True

# 🔒 Prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# 🔒 Cookies only sent over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# ---------------------------
#   STATIC FILES
# ---------------------------
STATIC_URL = 'static/'


# ---------------------------
#   CUSTOM USER MODEL
# ---------------------------
AUTH_USER_MODEL = 'bookshelf.CustomUser'

LOGIN_REDIRECT_URL = 'relationship_app:list_books'
LOGOUT_REDIRECT_URL = 'relationship_app:list_books'


# ---------------------------
#   DEFAULT PK
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
