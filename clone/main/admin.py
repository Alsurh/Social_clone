from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
from .models import Smeep

# Unregister groups
admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInLine(admin.StackedInline):
    model = Profile

# Estend user Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInLine]

# Unregister initial user
admin.site.unregister(User)
# Reregister User
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register smeeps
admin.site.register(Smeep)

