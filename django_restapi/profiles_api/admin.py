from django.contrib import admin
from profiles_api import models #import custom models
# Register your models here.

admin.site.register(models.UserProfile) #register custom model so it is displayed in the admin page of django
admin.site.register(models.ProfileFeedItem)