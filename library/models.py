from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
class School(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=255)
    director_name=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    contact=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'director_name', 'contact')
    search_fields = ('name', 'district', 'director_name__username')
    list_filter = ('district',)
    

class Book(models.Model):
    title=models.CharField(max_length=100)
    subject=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    year=models.IntegerField()
    price=models.IntegerField()
    isbn=models.CharField(max_length=100)

    def __str__(self):
     return self.title
    

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'year', 'isbn')
    search_fields = ('title', 'subject', 'isbn')
    list_filter = ('subject', 'grade', 'year')

class BookStock(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    total_quantity=models.IntegerField()
    available_quantity=models.IntegerField()
    
    def __str__(self):
       return f"Book: {self.book.title} -- total_quantity: {self.total_quantity} -- availble_quantity: {self.available_quantity}"


class BookStockAdmin(admin.ModelAdmin):
    list_display = ('book', 'total_quantity', 'available_quantity')
    search_fields = ('book__title',)
    list_filter = ('book__subject',)

class SchoolBook(models.Model):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    rent_price=models.IntegerField()
    def __str__(self):
     return f"Shool: {self.school.name} — Book: {self.book.title} -- quantity: {self.quantity}"

class SchoolBookInline(admin.TabularInline):
    model = SchoolBook
    extra = 1

class Student(models.Model):
    full_name=models.CharField(max_length=100)
    class_name=models.CharField(max_length=50)
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    def __str__(self):
     return self.full_name

class SchoolWithBooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'director_name')
    inlines = [SchoolBookInline]

class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'class_name', 'school')
    search_fields = ('full_name',)
    list_filter = ('school', 'class_name')



class BookIssue(models.Model):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    issue_date=models.DateTimeField()    
    return_date=models.DateTimeField()    
    returned=models.IntegerField()
    rent_price=models.IntegerField()
    status = models.CharField( max_length=20, choices=[
        ('issued', 'Issued'),
        ('returned', 'Returned'),]
)
    def __str__(self):
      return f"Student: {self.student.full_name} — Book: {self.book.title} -- status: {self.status}"
    


class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('student', 'school', 'book', 'issue_date', 'return_date', 'status')
    list_filter = ('status', 'school', 'book')
    search_fields = ('student__full_name', 'book__title', 'school__name')
    date_hierarchy = 'issue_date'



class UserRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('director', 'Director'),
        ('librarian', 'Librarian'),
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    linked_school=models.ForeignKey(School,on_delete=models.CASCADE,null=True,blank=True) 
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'linked_school')
    list_filter = ('role',)
    search_fields = ('user__username', 'linked_school__name')