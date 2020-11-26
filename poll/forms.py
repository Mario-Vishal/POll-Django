from django.forms import ModelForm
from .models import Poll, Options
from django.forms import formset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PollForm(ModelForm):

    class Meta:

        model = Poll

        fields = ['poll_question','option_number']


class OptionsForm(forms.Form):

    name = forms.CharField(
        label = "option",
        widget = forms.TextInput(attrs={
            'placeholder':'type option',
            'required':True,
            'class':'option-form'
        })
    )

class SignUpForm(UserCreationForm):


    class Meta:

        model = User
        fields = ["username","email","password1","password2"]

    def save(self,commit=True):

        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return user




# OptionsFormset = formset_factory(OptionsForm,extra=2)

    


