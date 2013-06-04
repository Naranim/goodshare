from django import forms
from goodshare.accounts.models import Account, Transaction, Comment


class AccountCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('alias',
                  'first_name',
                  'last_name',
                  'email',
                  'gender',
                  'date_of_birth')

    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            "alias",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "gender",
            "date_of_birth",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            raise forms.ValidationError("Bad passwords")

        return password1


    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['user', 'creator', 'date']

class AccountChangeForm(forms.ModelForm):
    pass

