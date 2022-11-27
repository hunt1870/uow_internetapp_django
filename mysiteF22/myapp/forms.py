from django import forms
from myapp.models import Order, Client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {'client': forms.RadioSelect()}
        labels = {'client': 'Client Name', 'num_units': 'Quantity'}


class InterestForm(forms.Form):
    INTEREST = [(1, "Yes"), (0, "No")]
    interested = forms.ChoiceField(choices=INTEREST, widget=forms.RadioSelect())
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=99999999)
    comments = forms.CharField(widget=forms.Textarea, label="Additional Comments", required=False)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'password', 'company', 'shipping_address',
                  'city', 'province', 'interested_in', 'image']
        widgets = {'interest_in': forms.CheckboxSelectMultiple()}
        labels = {'first_name': 'First name', 'last_name': 'Last name', 'shipping_address': 'Shipping address',
                  'interested_in': 'interested in', 'image': 'Profile picture'}

# class User(forms.Form):
#     username = forms.CharField(label="Username", max_length=30)
#     password = forms.CharField(widget=forms.PasswordInput(),label="Password")
