from django.forms import ModelForm
from .models import Poll, Options
from django.forms import formset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PollForm(forms.ModelForm):
    poll_question = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Type your poll question here!',
        'class':'poll-section row'
        }), label='')
    class Meta:
        model = Poll

        fields = [
            'poll_question'
        ]


class OptionsForm(forms.ModelForm):

    name = forms.CharField(label='',widget=forms.TextInput(attrs={
    'class':'option-form',
    'placeholder':'your option',
    'required':True}))

    class Meta:

        model = Options

        fields = [
            'name'
        ]


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




OptionsFormset = formset_factory(OptionsForm,extra=1)

    


