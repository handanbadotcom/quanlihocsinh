from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.


class LOPHOC(models.Model):
    TENLOP = models.CharField(max_length=30, null=False)
    SISO = models.IntegerField(null=False)
    NIENKHOA = models.CharField(max_length=10, null=False)
    
    def __str__(self):
        return self.TENLOP     

class HOCSINH(models.Model):
    HOTEN = models.CharField(max_length=300)
    NGAYSINH = models.DateField(null=False)
    GIOITINH_CHOICE = [
        ('M','male'),
        ('F','female')
    ]
    GIOITINH = models.CharField(max_length=5, choices=GIOITINH_CHOICE, blank=True, null=True)
    EMAIL = models.CharField(max_length=30, null=False)
    LOPHOC = models.ForeignKey(LOPHOC, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.HOTEN
    
class Subject(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Grade(models.Model):
    student = models.ForeignKey(HOCSINH, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    
    gr15m = models.FloatField(default=0)
    gr45m = models.FloatField(default=0)
    grExam = models.FloatField(default=0)
    semester = models.IntegerField(null=True)
    
    @property
    def AVG(self):
        avg = (self.gr15m + 2*self.gr45m + 3*self.grExam)/6
        return avg


class Age(models.Model):
    year = models.CharField(max_length=200, unique=True)
    max_age = models.IntegerField(null=False)
    min_age = models.IntegerField(null=False)

    def __str__(self):
        return self.year
