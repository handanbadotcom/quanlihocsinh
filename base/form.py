from django.forms import ModelForm
from .models import HOCSINH, LOPHOC, MONHOC


class HocSinhForm(ModelForm):
    class Meta:
        model = HOCSINH
        fields = '__all__'

class ClassForm(ModelForm):
    class Meta:
        model = LOPHOC
        fields = '__all__'

class SubjectForm(ModelForm):
    class Meta:
        model = MONHOC
        fields = '__all__'