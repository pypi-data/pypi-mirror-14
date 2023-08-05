from django.contrib import admin
from .models import VerifiedEmail

class VerifiedEmailAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'last_verified')

admin.site.register(VerifiedEmail, VerifiedEmailAdmin)
