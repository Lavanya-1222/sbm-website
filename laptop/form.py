from django import forms
from .models import Inventories

class InventoryForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=Inventories.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='Laptop'
    )

  

    class Meta:
        model = Inventories
        fields = ['category', 'item_name', 'quantity', 'price','software_type']

        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of Brands'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'software_type': forms.Select(attrs={
                'class': 'form-control',
                'min': 1
            }),
            
        }
