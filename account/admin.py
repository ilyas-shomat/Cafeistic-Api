from django.contrib import admin
from .models import Account, Establishment, Schedule

# Register your models here.
admin.site.register(Account)
admin.site.register(Establishment)
admin.site.register(Schedule)