from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(School)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(BookStock)
admin.site.register(SchoolBook)
admin.site.register(BookIssue)
admin.site.register(UserRole)