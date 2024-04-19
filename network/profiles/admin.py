from django.contrib import admin
from .models import Profile, Relationship
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        print(f"Deleting user: {obj}")
        super().delete_model(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Relationship)
