from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import *

admin.site.site_header = settings.TITLE
admin.site.site_title = settings.TITLE
admin.site.index_title = _('Welcome to Administration Panel')

admin.site.register(Problem)
