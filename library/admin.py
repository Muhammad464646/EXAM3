from django.contrib import admin
from .models import *
#


admin.site.register(School, SchoolWithBooksAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookStock, BookStockAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(BookIssue, BookIssueAdmin)
admin.site.register(UserRole, UserRoleAdmin)
