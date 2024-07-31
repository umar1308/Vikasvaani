from django.contrib import admin
from .models import user_data,quiz, Report, ngo,techcourse, engcourse
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUser(UserAdmin):
    model = user_data
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('userid',)}),
    )
    list_display=('userid','username','email','is_staff','last_login','date_joined','test_attempt','dob','contact','gender','profilelink1','profilelink2','profilelink3',"pfp")
# (model,function)
admin.site.register(user_data, CustomUser)
admin.site.register(quiz)
admin.site.register(Report)
admin.site.register(ngo)
admin.site.register(techcourse)
admin.site.register(engcourse)
