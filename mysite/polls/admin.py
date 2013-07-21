from django.contrib import admin
from polls.models import Poll

class PollAdmin(admin.ModelAdmin):
    pass

admin.site.register(Poll, PollAdmin)
