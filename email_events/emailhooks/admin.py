from django.contrib import admin

from emailhooks.models import DefaultEvent, OpenEvent, OpenMessage

admin.site.register(OpenMessage)
admin.site.register(DefaultEvent)
admin.site.register(OpenEvent)