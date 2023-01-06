from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import  *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import *
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import  User, HOCSINH, LOPHOC, Subject
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import HocSinhForm, ClassForm, SubjectForm

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
        
        while True:
            if name == '' or className == '':
                message = 'Vui lòng nhập đầy đủ thông tin!'
                print(message)
                break
            
            try:
                classRoom = LOPHOC.objects.get(TENLOP=className)
            except:
                message = 'Lớp học không tồn tại!'
                print(message)
                break
            
            try:
                student = HOCSINH.objects.get(HOTEN=name, LOPHOC=classRoom)
            except:
                message = 'Học sinh không tồn tại!'
                print(message)
                break
            
            i = 1
            while i <= 2:
                iSemesterGrades = Grade.objects.filter(student=student, semester=i)
                print(iSemesterGrades)
                iSemesterAVGs = []
                i+=1
                for subject in iSemesterGrades:
                    iSemesterAVGs.append(subject.AVG)
                    avg.append(round(sum(iSemesterAVGs)/len(iSemesterAVGs), 1))
            break
    
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
        print(request.POST)
        while True:
            if className == '' or subject == '' or semester == '':
                message = 'Vui lòng nhập đầy đủ thông tin!'
                break
            
            if semester != '1' and semester != '2':
                message = 'Chỉ có học kỳ I hoặc học kỳ II'
                break
                
            try:
                classRoom = LOPHOC.objects.get(TENLOP=className)
                print(classRoom)
            except:
                message = 'Lớp học không tồn tại!'
                print(message)
                break
                
            try:
                subject = Subject.objects.get(name=subject)
                print(subject)
            except:
                message = 'Môn học không tồn tại!'
                print(message)
                break
                
            students = HOCSINH.objects.filter(LOPHOC=classRoom)
            print(students)
            
            students = HOCSINH.objects.filter(LOPHOC=classRoom)
            
            for student in students:
                try:
                    grade = Grade.objects.get(student=student, subject=subject, semester=semester)
                    grades.append(grade)
                except:                     
                    grades.append(0)
                    continue
            break
    
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
    lophoc = LOPHOC.objects.all()
    hs = HOCSINH.objects.all()
    if request.method == 'POST':
        usernames = request.POST.getlist('HOTEN')
        cl = request.POST.get('lop')
        class_list = LOPHOC.objects.all()
        print(usernames)
        studentsInClass = HOCSINH.objects.filter(LOPHOC__TENLOP=cl)
        LOP = LOPHOC.objects.get(TENLOP=cl)
        print(len(studentsInClass) + len(usernames))
        if LOP.SISO >= (len(studentsInClass) + len(usernames)):
           for username in usernames:
                    student = HOCSINH.objects.get(HOTEN=username)
                    student.LOPHOC=LOP
                    student.save()
                    messages.success(request, "Thêm thành công")
                   # return redirect(reverse('lapDSLop', kwargs={'age_id': age_id}))
        else:
                    messages.success(request, "Số lượng học sinh vượt quá qui định")


    context = {
        'students': hs,
        'lop': lophoc
    }
    return render(request, 'base/lapDSlop.html', context=context)

# Class setting -----------
def class_setting(request):
    form = ClassForm()
    classInfo = LOPHOC.objects.all().values()
    if request.method=='POST':
        print(request.POST)
        LOPHOC.objects.create(
            TENLOP=request.POST.get('TENLOP'),
            SISO=request.POST.get('SISO'),
            NIENKHOA_id=request.POST.get('NIENKHOA'),
        )
        return redirect('class_setting')

    context = {
        'form':form,
        'classInfo':classInfo,
        }

    return render(request, 'base/class_setting.html',context)

def class_setting_delete(request, pk):
    form = ClassForm()
    classRoom = LOPHOC.objects.filter(id=pk).values()
    classList = LOPHOC.objects.all().values()

    if request.method=='POST':
        LOPHOC.objects.get(id=pk).delete()
        return redirect('class_setting')

    context = {
        'form':form,
        'classRoom':classRoom,
        'classList':classList,
        }

    return render(request, 'base/class_setting_delete.html',context)

def class_setting_update(request, pk):
    form = SubjectForm()
    classRoom = LOPHOC.objects.get(id=pk)
    classList = LOPHOC.objects.all().values()

    if request.method=='POST':
        print(request.POST)
        name = request.POST['TENLOP']
        number = request.POST['SISO']
        classRoom = LOPHOC.objects.get(id=pk)    
        classRoom.TENLOP = name
        classRoom.SISO = number
        classRoom.save()    
        return redirect('class_setting')

    context = {
        'form':form,
        'classRoom':classRoom,
        'classList':classList,
        }

    return render(request, 'base/class_setting_update.html',context)

# Subject setting -----------
def subject_setting(request):
    form = SubjectForm()
    subjectInfo = Subject.objects.all().values()

    if request.method=='POST':
        print(request.POST)
        Subject.objects.create(
            name=request.POST.get('name'),
            DIEMCHUAN=request.POST.get('DIEMCHUAN'),
        )
        return redirect('subject_setting')

    context = {
        'form':form,
        'classInfo':subjectInfo,
        }

    return render(request, 'base/subject_setting.html',context)

def subject_setting_delete(request, pk):
    form = SubjectForm()
    subject = Subject.objects.filter(id=pk).values()
    subjectList = Subject.objects.all().values()

    if request.method=='POST':
        Subject.objects.get(id=pk).delete()
        return redirect('subject_setting')

    context = {
        'form':form,
        'subject':subject,
        'subjectList':subjectList,
        }

    return render(request, 'base/subject_setting_delete.html',context)

def subject_setting_update(request, pk):
    form = SubjectForm()
    subject = Subject.objects.get(id=pk)
    subjectList = Subject.objects.all().values()

    if request.method=='POST':
        print(request.POST)
        name = request.POST['TENMONHOC']
        marks = request.POST['DIEMCHUAN']
        subject = Subject.objects.get(id=pk)    
        subject.name = name
        subject.DIEMCHUAN = marks
        subject.save()    
        return redirect('subject_setting')

    context = {
        'form':form,
        'subject':subject,
        'subjectList':subjectList,
        }

    return render(request, 'base/subject_setting_update.html',context)

