from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

# mix profile & user info
class ProfileInline(admin.StackedInline):
    model = Profile

# extend the user model 
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# un-register the old way
# admin.site.unregister(User)

# re-register the new way
# admin.site.register(User, UserAdmin)