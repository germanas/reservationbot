from django import forms

from .models import Registration

class reg_form(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ('name', 'surname', 'registration_date', 'registration_time', 'user')
