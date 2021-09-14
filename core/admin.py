from core.views import contact
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ContactLink)
admin.site.register(Contact)
admin.site.register(NewsLetters)
admin.site.register(FeedBack)
admin.site.register(UserProfile)
admin.site.register(Note)

admin.site.site_header = "Note Website "
admin.site.site_title = "Note Website admin panel"
admin.site.index_title = "Welcome to note website admin panel"


