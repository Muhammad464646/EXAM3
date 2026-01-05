from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import UserRole,School,SchoolBook,BookStock,Student,BookIssue, Book
from .decorators import role_required

def login_view(request):
    if request.method=='GET':
     return render(request,'login.html')
    elif request.method=='POST':
       username=request.POST.get('username')
       password=request.POST.get('password')
       
       user=authenticate(request,username=username,password=password)
       if user:
        login(request,user)
        return redirect_by_role(user)
    return render(request, 'login.html', {
            'error': 'Неверный логин или пароль'
        })

def logout_view(request):
    if request.method=='POST':
     logout(request)
     return redirect('')


def redirect_by_role(user):
    role = user.userrole.role

    if role == 'admin':
        return redirect('schools')

    if role == 'director':
        return redirect('BookIssiue')

    if role == 'librarian':
        return redirect('controlB')
    
@role_required(['librarian'])
def control_book(request):
    books=Book.objects.all()

    title_query = request.GET.get('title', '')
    subject_query = request.GET.get('subject', '')
    grade_query = request.GET.get('grade', '')
    subjects = Book.objects.values_list('subject', flat=True).distinct()
    grades = Book.objects.values_list('grade', flat=True).distinct()

    if title_query:
        books = books.filter(title__icontains=title_query)
    if subject_query:
        books = books.filter(subject=subject_query)
    if grade_query:
        books = books.filter(grade=grade_query)
    if request.method=='POST':
       title=request.POST.get('title')
       subject=request.POST.get('subject')
       grade=request.POST.get('grade')
       year=request.POST.get('year')
       isbn=request.POST.get('isbn')
       Book.objects.create(
          title=title,
          subject=subject,
          grade=grade,
          year=year,
          isbn=isbn
       )
    return render(request,'control_book.html',context={'books':books,'title_query': title_query,
        'subject_query': subject_query,
        'grade_query': grade_query,
        'subjects': subjects,
        'grades': grades,})

@role_required(['admin'])
def schools_view(request):
    name_query = request.GET.get('name', '')
    school=School.objects.all()
    if name_query:
      school = school.filter(name__icontains=name_query) 
    if request.method == "POST":
        name = request.POST.get("name")
        district = request.POST.get("district")
        director_name = request.POST.get("director_name")
        contact = request.POST.get("contact")
        
        if name and district and director_name and contact:
            School.objects.create(
                name=name,
                district=district,
                director_name=director_name,
                contact=contact
            )
            return redirect('schools')
    return render(request,'school.html',context={'school':school,'name_query': name_query,})

@role_required(['director', 'librarian'])
def BookIssiuе(request):
    schools = School.objects.all()
    selected_school_id = request.GET.get('school_id')

    students = Student.objects.none()   # пустой QuerySet по умолчанию
    books1 = SchoolBook.objects.none()  # пустой QuerySet по умолчанию

    if selected_school_id:
        students = Student.objects.filter(school_id=selected_school_id)
        books1 = SchoolBook.objects.filter(school_id=selected_school_id)

    if request.method == 'POST':
        school_id = request.POST.get('school_id')
        student_id = request.POST.get('student_id')
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity'))
        issue_date = request.POST.get('issue_date')
        return_date = request.POST.get('return_date')

        school = get_object_or_404(School, id=school_id)
        student = get_object_or_404(Student, id=student_id)
        school_book = get_object_or_404(SchoolBook, school=school, book_id=book_id)

        BookIssue.objects.create(
            student=student,
            school=school,
            book=school_book.book,
            issue_date=issue_date,
            return_date=return_date,
            status='issued'
        )
        school_book.quantity -= quantity
        school_book.save()

        return redirect('BookIssiue')

    return render(request, 'BookIssue.html', {
        'schools': schools,
        'selected_school_id': int(selected_school_id) if selected_school_id else None,
        'students': students,
        'books1': books1
    })



def edit_book(request):
    if request.method == 'POST':
        book = Book.objects.get(id=request.POST['book_id'])
        book.title = request.POST['title']
        book.subject = request.POST['subject']
        book.grade = request.POST['grade']
        book.year = request.POST['year']
        book.isbn = request.POST['isbn']
        book.save()

    return redirect('controlB')


def delete_book(request):
    if request.method == 'POST':
        Book.objects.filter(id=request.POST['book_id']).delete()
    return redirect('controlB')


@role_required(['admin'])
def users_view(request):
    users = User.objects.all().select_related('userrole') 
    roles = UserRole.objects.values_list('role', flat=True).distinct()
    name_query = request.GET.get('name', '')
    role_query = request.GET.get('role', '')
    
    if name_query:
        users = users.filter(username__icontains=name_query) 
    
    if role_query:
        users = users.filter(userrole__role=role_query) 
    
    schools = School.objects.all()
    
    return render(request, 'users.html', {
        'users': users,
        'schools': schools,
        'role_query': role_query,
        'roles': roles,
        'name_query': name_query
    })

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        school_id = request.POST.get("school")
        user = User.objects.create_user(username=username,password=password)
        school = get_object_or_404(School, id=school_id)
        UserRole.objects.create(
            user=user,
            role=role,
            linked_school=school,
        )

    return redirect('users')



def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        user.delete()  
    return redirect('users')



def no_access(request):
    return render(request, 'no_access.html')