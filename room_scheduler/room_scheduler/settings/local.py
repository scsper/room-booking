"""
local settings to be modified for development
"""

from .base import *
import os

DEBUG = True
TEMPLATE_DEBUG = True


EMAIL_HOST = "localhost"
EMAIL_PORT = 1025


DATABASES = {
	"default": {
		'ENGINE': 'django.db.backends.sqlite3',
		"NAME": os.path.join(BASE_DIR, 'room_scheduler_db.sqlite3'),
	}
}


INTERNAL_IPS = ("127.0.0.1",)