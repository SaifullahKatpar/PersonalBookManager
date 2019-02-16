from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'id': 'search', 'placeholder':'Search Books and Authors'}))
    search_by = forms.ChoiceField(choices=['Author','Book'])
    
