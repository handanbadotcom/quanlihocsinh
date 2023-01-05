from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.


class LOPHOC(models.Model):
    TENLOP = models.CharField(max_length=30, null=False)
    SISO = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    NIENKHOA = models.CharField(max_length=10, null=False, validators=[MinValueValidator(1900), MaxValueValidator(3000)])      
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
    LOPHOC = models.ManyToManyField(LOPHOC, blank=True)

    def __str__(self):
        return self.HOTEN

class MONHOC(models.Model):
    TENMONHOC = models.CharField(max_length=50)
    DIEMCHUAN = models.FloatField(null=False, default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    def __str__(self):
        return self.TENMONHOC