from django import forms
from .models import Item, ClaimRequest


class ItemForm(forms.ModelForm):
    date_reported = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='When was the item lost or found?'
    )

    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'item_type', 'location', 'date_reported', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Blue Samsung Galaxy S24'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed description including color, brand, distinguishing features...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'item_type': forms.RadioSelect(),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Library 2nd Floor, Central Park Gate 3'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'item_type': 'Report Type',
            'date_reported': 'Date Lost/Found',
        }


class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain how you can prove this item belongs to you...'
            }),
        }
        labels = {
            'message': 'Your Claim Message',
        }


class ItemSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Search items...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Item.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    item_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types'), ('lost', 'Lost'), ('found', 'Found')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
