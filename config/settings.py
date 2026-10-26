import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# En Vercel definí SECRET_KEY como variable de entorno (Settings > Environment Variables)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-cambiala-en-produccion")
DEBUG = os.environ.get("DEBUG", "0") == "1"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

# Si tenés dominio propio: DOMINIO=midominio.com
if os.environ.get("DOMINIO"):
    ALLOWED_HOSTS.append(os.environ["DOMINIO"])
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['DOMINIO']}")

# Sin base de datos: la calculadora no guarda nada (ideal para serverless)
INSTALLED_APPS = ["estadistica"]
DATABASES = {}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"  # Vercel lee esto para encontrar la app

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    }
]

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
