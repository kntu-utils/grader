from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *

admin.site.site_header = _('Grader')
admin.site.site_title = _('Grader')
admin.site.index_title = _('Welcome to Grader')

admin.site.register(Problem)
