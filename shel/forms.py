import span as span
from crispy_forms.bootstrap import FormActions
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from shel.models import *
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML


class MemberRegModelForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = Person
        exclude = ['user']
        fields = ['displayed_name', 'image']

    def __init__(self, *args, **kwargs):
        super(MemberRegModelForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['displayed_name'].widget.attrs.update({'placeholder': 'Name to Be Displayed'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Password Again'})

    def clean_password(self):
        if len(self.cleaned_data['password']) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return self.cleaned_data['password']

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if not password or not password2 or password != password2:
            raise forms.ValidationError('Entered passwords don\'t match.')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            msg = 'username is taken ! '
            raise forms.ValidationError(_(msg), code='invalid')
        return username

    def save(self, commit=True):
        person = super(MemberRegModelForm, self).save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        user.save()
        person.user = user
        person.save()
        return person


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('login', 'login'),
            )
        )


class GroupRegModelForm(forms.ModelForm):

    class Meta:
        model = Group

        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GroupRegModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'group name'})

    def clean_name(self):
        if len(self.cleaned_data['name']) < 2:
            raise forms.ValidationError('name must be at least 2 characters long.')
        return self.cleaned_data['name']

    def clean_username(self):
        group_name = self.cleaned_data['name']
        if User.objects.filter(namegrp=group_name).exists():
            msg = 'group name is taken ! '
            raise forms.ValidationError(_(msg), code='invalid')
        return group_name

    def save(self, commit=True):
        group = super(GroupRegModelForm, self).save(commit=False)
        group.admin = self.user
        group.save()
        return group


class EditProfileForm(forms.ModelForm):
    displayed_name = forms.CharField(label='displayed_name')
    image = forms.ImageField(label='image')

    class Meta:
        model = Person
        fields = ['displayed_name', 'image']