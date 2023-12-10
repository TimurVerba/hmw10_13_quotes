from django import forms
from django.contrib.postgres.fields import ArrayField
from django.forms import TextInput

from .models import Author, Quote


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    tags = TextInput(attrs={'class': 'form-control'})
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Author',
    )
    quote = TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = Quote
        fields = ['tags', 'author', 'quote']
