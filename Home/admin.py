from django.contrib import admin
from .models import Profile, Virtue
from .models import Team, TeamRequest, Event
# Register your models here.


admin.site.register(Team)
admin.site.register(TeamRequest)
admin.site.register(Profile)
admin.site.register(Virtue)
admin.site.register(Event)