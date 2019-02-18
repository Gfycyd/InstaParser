from django import forms
class QueryForm(forms.Form):
    q = forms.CharField(label='Запрос ',  max_length=100)
class QueryCount(forms.Form):
    count = forms.CharField(label='Количество:', max_length=100)