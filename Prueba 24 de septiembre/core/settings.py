import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "solo-desarrollo-cambiar-en-produccion")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "productos", "cuentas"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "core.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates", "DIRS":[BASE_DIR / "templates"], "APP_DIRS":True, "OPTIONS":{"context_processors":["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "core.wsgi.application"
if os.getenv("DB_ENGINE", "mysql") == "sqlite":
    DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3", "NAME":BASE_DIR / "db.sqlite3"}}
else:
    DATABASES = {"default":{"ENGINE":"django.db.backends.mysql", "NAME":os.getenv("DB_NAME", "tienda_mascotas_db"), "USER":os.getenv("DB_USER", "root"), "PASSWORD":os.getenv("DB_PASSWORD", ""), "HOST":os.getenv("DB_HOST", "127.0.0.1"), "PORT":os.getenv("DB_PORT", "3306"), "OPTIONS":{"charset":"utf8mb4"}}}
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="es-cl"
TIME_ZONE="America/Santiago"
USE_I18N=True
USE_TZ=True
STATIC_URL="static/"
STATICFILES_DIRS=[BASE_DIR / "static"]
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
LOGIN_URL="login"
LOGIN_REDIRECT_URL="gestion_productos"
LOGOUT_REDIRECT_URL="inicio"

# --- Correo para el registro con token ---
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "no-responder@patitas.local")
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # el enlace del correo vence en 24 horas
