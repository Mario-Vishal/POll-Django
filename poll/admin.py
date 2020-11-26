from django.contrib import admin
from .models import Poll,Options
# Register your models here.
admin.site.register(Poll)
admin.site.register(Options)