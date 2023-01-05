from django.forms import ModelForm
from .models import HOCSINH
from .models import LOPHOC

class HocSinhForm(ModelForm):
    class Meta:
        model = HOCSINH
        fields = '__all__'

class LopHocForm(ModelForm):
    class Meta:
        model = LOPHOC
        fields = '__all__'