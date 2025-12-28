from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address', 'city', 'postal_code']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'placeholder': 'Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'placeholder': 'you@example.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'rows': 3,
                'placeholder': 'Street Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'placeholder': 'City'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm',
                'placeholder': 'Postal Code'
            }),
        }
