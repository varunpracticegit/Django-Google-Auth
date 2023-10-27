from django.contrib import admin
from .models import LoginLogoutHistory

class LoginLogoutHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time')
    list_filter = ('user', 'login_time', 'logout_time')
    search_fields = ('user__username', 'login_time', 'logout_time')

# Register the model with the custom admin class
admin.site.register(LoginLogoutHistory, LoginLogoutHistoryAdmin)
