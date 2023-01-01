from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import  *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import *
from django.urls import reverse, reverse_lazy


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    context={}
    return render(request, 'base/home.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
           messages.error(request, 'User not found')

        user = authenticate(request, username=username, password=password)

        if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context= {}
    return render(request, 'base/login.html', context)

def registerPage(request):
    page='register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Error occured')
    return render(request, 'base/signup.html', {'form':form, 'page':page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def TiepnhanHS(request):
    form =HocSinhForm()
    gioitinh = 'male'
    if request.method=='POST':
        gender=request.POST.get('GIOITINH')
        print(gender)
        HOCSINH.objects.create(
            HOTEN=request.POST.get('HOTEN'),
            GIOITINH=gender,#request.POST.get('GIOITINH'),
            NGAYSINH= request.POST.get('NGAYSINH'),
            EMAIL= request.POST.get('EMAIL'),
        )
        return redirect('home')
    context = {'form':form}
    return render(request, 'base/TiepnhanHS.html', context)

def searchStudent(request):
    message = None
    student = None
    avg = []
    
    if request.method == 'POST':
        name = request.POST.get('name')
        className = request.POST.get('class')
        classRoom = LOPHOC.objects.get(TENLOP=className)
        
        try:
            student = HOCSINH.objects.get(HOTEN=name, LOPHOC=classRoom)
        except:
            message = 'Student does not exist!'
        i = 1
        while i <= 2:
            iSemesterGrades = Grade.objects.filter(student=student, semester=i)
            print(iSemesterGrades)
            iSemesterAVGs = []
            i+=1
            for subject in iSemesterGrades:
                iSemesterAVGs.append(subject.AVG)
            avg.append(round(sum(iSemesterAVGs)/len(iSemesterAVGs), 1))
    
    
    context = {'student': student, 'message': message, 'avg': avg}
    return render(request, 'base/search_student.html', context)

def receiveTranscripts(request):
    message = None
    classRoom = None
    students = []
    grades = []
    
    if request.method == 'POST':
        className = request.POST.get('class')
        subject = request.POST.get('subject')
        semester = request.POST.get('semester')
        
        try:
            classRoom = LOPHOC.objects.get(TENLOP=className)
        except:
            message = 'Class does not exist!'
            
        students = HOCSINH.objects.filter(LOPHOC=classRoom)
        subject = Subject.objects.get(name=subject)
        
        for student in students:
            grade = Grade.objects.get(student=student, subject=subject, semester=semester)
            grades.append(grade)
    
    context = {'message': message, 'students': students, 'grades': grades}
    return render(request, 'base/receive_transcripts.html', context)
    


def quanlidotuoi(request):
    age = Age.objects.all()
    context = {'age': age}
    return render(request, 'base/quanlidotuoi.html', context=context)



def capNhatTuoi(request, age_id):
    age = get_object_or_404(Age, id=age_id)
    form = ageForm(request.POST or None, instance=age)
    context = {
        'form': form,
        'subject_id': age_id,
        'page_title': 'capNhatTuoi'
    }
    if request.method == 'POST':
        if form.is_valid():
            year = form.cleaned_data.get('year')
            max_age = form.cleaned_data.get('max_age')
            min_age = form.cleaned_data.get('min_age')
            if max_age < min_age:
                messages.error(request, "Could Not Update")
                return render(request, "base/capNhatTuoi.html", context)
            else:
                try:
                    Year = Age.objects.get(id=age.id)
                    Year.year = year
                    Year.max_age = max_age
                    Year.min_age = min_age
                    Year.save()
                    messages.success(request, "Cập nhật thành công")
                    return redirect(reverse('quanlidotuoi'))
                except Exception as e:
                    messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Hãy điều đầy đủ vào ô thông tin !!!")
    else:
        return render(request, "base/capNhatTuoi.html", context)



def xoaTuoi(request, age_id):
    age = get_object_or_404(Age, id=age_id)
    age.delete()
    messages.success(request, "Age deleted successfully!")
    return redirect(reverse('quanlidotuoi'))



def themTuoi(request):
    form = ageForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'themTuoi'
    }
    if request.method == 'POST':
        if form.is_valid():
            year = form.cleaned_data.get('year')
            max_age = form.cleaned_data.get('max_age')
            min_age = form.cleaned_data.get('min_age')
            if max_age < min_age:
                messages.error(request, "Could Not Add")
                render(request, 'base/themTuoi.html', context)
            else:
                try:
                    Year = Age()
                    Year.year = year
                    Year.max_age = max_age
                    Year.min_age = min_age
                    Year.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('quanlidotuoi'))
                except:
                    messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Lỗi định dạng")
    return render(request, 'base/themTuoi.html', context)



semester = 2

def nienkhoa(request):
    form = YearForm()
    age = Age.objects.all()
    context = {
        'form': form,
        'age': age
    }
    return render(request, 'base/nienkhoa.html', context=context)



def lapDSlop(request, age_id):
    lophoc = LOPHOC.objects.all
    hs = HOCSINH.objects.all
    if request.method == 'POST':
        usernames = request.POST.getlist('username_class')
        cl = request.POST.get('TENLOP')
        class_list = LOPHOC.objects.all()
        for lop in class_list:
            if lop.TENLOP == cl:
                studentsInClass = HOCSINH.objects.filter(lop__TENLOP=cl)
                if lop.max_number >= (len(studentsInClass) + len(usernames)):
                    for username in usernames:
                        student = HOCSINH.objects.get(user__username=username)
                        student.LOPHOC.add(lop)
                        student.save()
                    messages.success(request, "Thêm thành công")
                    return redirect(reverse('lapDSLop', kwargs={'age_id': age_id}))
                else:
                    messages.success(request, "Số lượng học sinh vượt quá qui định")
    context = {
        'students': hs,
        'lop': lophoc
    }
    return render(request, 'base/lapDSlop.html', context=context)


