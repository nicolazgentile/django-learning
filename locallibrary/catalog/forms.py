from django import forms
from django.core.exceptions import ValidationError

from .models import Client, Employee


class ClientForm(forms.ModelForm):
    easdxtra_field = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Client
        fields = '__all__'

    def clean(self):
        super(ClientForm, self).clean()

        first_name = self.cleaned_data.get('last_name')
        identification = self.cleaned_data.get('identification')
        if len(first_name) > 5:
            self._errors['last_name'] = self.error_class(['El ape es mooooooy largo'])

        if '666' in str(identification):
            raise ValidationError("Vo so loco, so? Pusite el namberbist chavón!!!")

        return self.cleaned_data


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
