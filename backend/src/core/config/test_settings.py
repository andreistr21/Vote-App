from core.settings import *

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

INSTALLED_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "vote",
]

DEBUG = False
