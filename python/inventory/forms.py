from django import forms
from .models import PurchaseOrder, PurchaseOrderItem, StockOut, StockOutItem
from products.models import Book

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'notes']
        widgets = {
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['book', 'quantity', 'unit_price']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StockOutItemForm(forms.ModelForm):
    class Meta:
        model = StockOutItem
        fields = ['book', 'quantity', 'unit_price']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        book = self.cleaned_data['book']
        if quantity > book.stock:
            raise forms.ValidationError(f'Số lượng xuất không được vượt quá tồn kho ({book.stock})')
        return quantity 