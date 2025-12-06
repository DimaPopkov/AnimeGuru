from django.templatetags.static import static

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v-&chg7*o7#(zvh3i%880p86(t5guy!20c%&0k)6xef6u1v^@9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['26.99.193.114', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',

    "crispy_forms",

    'main',
    'login',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

UNFOLD = {
    "LOGIN": {
        "image": lambda request: static("img/admin-login-background.jpg"),
    },
    "SHOW_LANGUAGES": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "main.admin.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Groups and Users"),
                "separator": False,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Users Activity Logs"),
                        "icon": "link",
                        "link": reverse_lazy("admin:main_useractivitylog_changelist"),
                    },
                ],
            },
            {
                "title": _("Main"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:main_product_changelist"),
                    },
                    {
                        "title": _("Category"),
                        "icon": "list",
                        "link": reverse_lazy("admin:main_category_changelist"),
                    },
                    {
                        "title": _("Tags"),
                        "icon": "list",
                        "link": reverse_lazy("admin:main_tags_changelist"),
                    },
                    {
                        "title": _("Pics"),
                        "icon": "link",
                        "link": reverse_lazy("admin:main_pics_changelist"),
                    },
                    {
                        "title": _("Status"),
                        "icon": "list",
                        "link": reverse_lazy("admin:main_status_changelist"),
                    },
                    {
                        "title": _("Weblinks"),
                        "icon": "list",
                        "link": reverse_lazy("admin:main_weblinks_changelist"),
                    },
                    {
                        "title": _("Voice_maker"),
                        "icon": "list",
                        "link": reverse_lazy("admin:main_voice_maker_changelist"),
                    },
                    {
                        "title": _("Characters"),
                        "icon": "people",
                        "link": reverse_lazy("admin:main_characters_changelist"),
                    },
                    {
                        "title": _("Comments"),
                        "icon": "comment",
                        "link": reverse_lazy("admin:main_comments_changelist"),
                    },
                ],
            },
        ]
    },
    "COLORS": {
        "base": {
            "50": "rgb(245, 245, 245)",
            "100": "rgb(200, 200, 200)",
            "200": "rgb(200, 200, 200)",
            "300": "rgb(200, 200, 200)",
            "400": "rgb(185, 185, 185)",
            "500": "rgb(170, 170, 170)",
            "600": "rgb(155, 155, 155)",
            "700": "rgb(140, 140, 140)",
            "800": "rgb(100, 100, 100)",
            "900": "rgb(30, 30, 30)",
            "950": "rgb(95, 95, 95)",
        },
        "primary": {
            "50": "rgb(230, 230, 230)",
            "100": "rgb(215, 215, 215)",
            "200": "rgb(200, 200, 200)",
            "300": "rgb(185, 185, 185)",
            "400": "rgb(170, 170, 170)",
            "500": "rgb(150, 150, 150)",
            "600": "rgb(140, 140, 140)",
            "700": "rgb(125, 125, 125)",
            "800": "rgb(110, 110, 110)",
            "900": "rgb(95, 95, 95)",
            "950": "rgb(80, 80, 80)",
        },
    },
    "BORDER_RADIUS": "10px",
}

CRISPY_TEMPLATE_PACK = "unfold_crispy"

CRISPY_ALLOWED_TEMPLATE_PACKS = ["unfold_crispy"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "main" / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("ru-ru", _("Russian")),
    ("en-en", _("English")),
    ("de-de", _("German")),
    #("po", _("Polish")),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'