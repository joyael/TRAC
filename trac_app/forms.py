from django import forms
from django.core.validators import MaxLengthValidator,MinValueValidator, RegexValidator
from .models import Role, RUser, Product

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'level']  # Specify the fields you want in the form


class RUserForm(forms.ModelForm):
    class Meta:
        model = RUser
        fields = ['username', 'hashed_password', 'role']  # Specify the fields you want in the form
        labels = {
            'hashed_password': 'Password',  # Change the label here
        }
        widgets = {
            'hashed_password': forms.PasswordInput(render_value=True)
        }

class RUserLoginForm(forms.ModelForm):
    class Meta:                                                                       
        model = RUser
        fields = ['username', 'hashed_password']  # Specify the fields you want in the form
        labels = {
            'hashed_password': 'Password',  # Change the label here
        }
        widgets = {
            'hashed_password': forms.PasswordInput(render_value=True)
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'tag', 'price']  # Specify the fields you want in the form

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # You can customize the form fields here if needed
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['tag'].widget.attrs.update({'placeholder': 'Enter product tag'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter product price'})


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'tag', 'price']  # Specify the fields you want to include in the form