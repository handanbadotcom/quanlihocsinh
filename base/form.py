from django.forms import ModelForm
from .models import HOCSINH

class HocSinhForm(ModelForm):
    class Meta:
        model = HOCSINH
        fields = '__all__'