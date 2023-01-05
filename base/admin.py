from django.contrib import admin
from .models import LOPHOC, HOCSINH, Subject, Grade, Age
# Register your models here.

admin.site.register(LOPHOC)
admin.site.register(HOCSINH)
admin.site.register(Age)
admin.site.register(Subject)
admin.site.register(Grade)
