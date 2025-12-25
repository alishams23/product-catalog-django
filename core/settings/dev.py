"""Development settings."""
from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = env(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"],
)
