# myapp/admin.py
from django.contrib import admin
from users.models import User, PasswordReset

admin.site.register(User)
admin.site.register(PasswordReset)
