from django import forms
from .models import Employee, Contact
import datetime

class EmpForm(forms.ModelForm):
    d_o_j = forms.DateField(
        label='What is your birth date?',
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(2005, datetime.date.today().year))
    )

    def __init__(self, *args, **kwargs):
        super(EmpForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Employee
        fields = '__all__'

        # field level validation
        # def clean_name(self):
        #     name = self.cleaned_data.get("name")
        #     if not str(name).isalnum():
        #         raise forms.ValidationError("Not a valid name")
        #     return name


class ContactModelForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


