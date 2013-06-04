from django import forms
from goodshare.goods.models import *


class GoodSearchForm(forms.ModelForm):

    class Meta:
        model = Good
        exclude = ['description', 'type']

    type = forms.ModelChoiceField(queryset=Type.objects.all())

    def __init__(self, *args, **kwargs):
        super(GoodSearchForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False


class GoodCreateForm(forms.ModelForm):

    class Meta:
        model = Good
