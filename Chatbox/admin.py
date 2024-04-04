from django.contrib import admin
from .models import Chatb

# Register your models here.

class chatbadmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'response', 'created_at']
    
    
    
admin.site.register(Chatb, chatbadmin)
    