
from django.forms import ModelForm, forms
from .models import *


class HocSinhForm(ModelForm):
    class Meta:
        model = HOCSINH
        fields = '__all__'

class ageForm(ModelForm):
    class Meta:
        model = Age
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ageForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_age'].widget.attrs.update({'class': 'form-control'})
        self.fields['min_age'].widget.attrs.update({'class': 'form-control'})

class YearForm(ModelForm):
    try:
        year_choices = set([(a, a.year) for a in Age.objects.all()])
        year = forms.CharField(label="",widget=forms.Select(
            choices=year_choices, 
            attrs={'class': 'form-select'
        }))
    except:
        ''''''
    class Meta:
        model = Age
        fields = ['year']


class ClassForm(ModelForm):
    class Meta:
        model = LOPHOC
        fields = '__all__'

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class GradeForm(ModelForm):
     class Meta:
        model = Grade
        fields = '__all__'
