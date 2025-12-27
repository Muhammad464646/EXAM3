from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=255)
    director_name=models.CharField(max_length=50)
    contact=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title=models.CharField(max_length=100)
    subject=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    year=models.IntegerField()
    isbn=models.CharField(max_length=100)

    def __str__(self):
     return self.title

class BookStock(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    total_quantity=models.IntegerField()
    available_quantity=models.IntegerField()
    
    def __str__(self):
       return f"Book: {self.book.title} -- total_quantity: {self.total_quantity} -- availble_quantity: {self.available_quantity}"

class SchoolBook(models.Model):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
     return f"Shool: {self.school.name} — Book: {self.book.title} -- quantity: {self.quantity}"


class Student(models.Model):
    full_name=models.CharField(max_length=100)
    class_name=models.CharField(max_length=50)
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    

    def __str__(self):
     return self.full_name

class BookIssue(models.Model):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    issue_date=models.DateTimeField()    
    return_date=models.DateTimeField()    
    status = models.CharField( max_length=20, choices=[
        ('issued', 'Issued'),
        ('returned', 'Returned'),]
)
    def __str__(self):
      return f"Student: {self.student.full_name} — Book: {self.book.title} -- status: {self.status}"
    

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