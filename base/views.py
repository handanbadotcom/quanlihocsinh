from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  User, HOCSINH, LOPHOC
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import HocSinhForm, LopHocForm

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


def class_setting(request):
    form = LopHocForm()
    classInfo = LOPHOC.objects.all().values()

    if request.method=='POST':
        LOPHOC.objects.create(
            TENLOP=request.POST.get('TENLOP'),
            SISO=request.POST.get('SISO'),
            NIENKHOA=request.POST.get('NIENKHOA'),
        )
        return redirect('class_setting')

    context = {
        'form':form,
        'classInfo':classInfo,
        }

    return render(request, 'base/class_setting.html',context)

def class_setting_delete(request, pk):
    form = LopHocForm()
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
    form = LopHocForm()
    classRoom = LOPHOC.objects.get(id=pk)
    classList = LOPHOC.objects.all().values()

    if request.method=='POST':
        name = request.POST['TENLOP']
        number = request.POST['SISO']
        year = request.POST['NIENKHOA']
        classRoom = LOPHOC.objects.get(id=pk)    
        classRoom.TENLOP = name
        classRoom.SISO = number
        classRoom.NIENKHOA = year
        classRoom.save()    
        return redirect('class_setting')

    context = {
        'form':form,
        'classRoom':classRoom,
        'classList':classList,
        }

    return render(request, 'base/class_setting_update.html',context)