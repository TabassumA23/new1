from django import forms
#from .models import Hobby

# Form for letting user log in
class LoginForm(forms.Form):
    username = forms.CharField(label="Username ", required="true", max_length=100)
    password = forms.CharField(
        label="Password ", 
        max_length=100,
        required="true",
        # Adding a password widget for password 
        widget=forms.PasswordInput()
    )

# Form for letting user change password
class UpdatePassForm(forms.Form):
    username = forms.CharField(label="Username ", required="true", max_length=100)
    password = forms.CharField(
        label="New password ", 
        max_length=100,
        required="true",
        # Adding a password widget for password 
        widget=forms.PasswordInput()
    )

# Form for letting user change username 
class UpdateUserForm(forms.Form):
    current_username = forms.CharField(label="Username ", required="true", max_length=100)
    new_username = forms.CharField(
         
        max_length=100,
        required="true",
        label="New Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter new username"}),
        
    )


# Form for letting user sign up
class SignUpForm(forms.Form):
    first_name = forms.CharField(label="First Name ", max_length=100, required="true")
    last_name = forms.CharField(label="Last Name ", max_length=100, required="true")
    username = forms.CharField(label="Username ", max_length=100, required="true")
    email = forms.EmailField(label="Email ", required="true")
    date_of_birth = forms.DateField(
        label="Date Of Birth ",
        required="true",
        # Adding a calendar widget for easier date entry
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    password = forms.CharField(
        label="Password ", required="true", max_length=100,
        # Adding a password widget for password 
        widget=forms.PasswordInput()
    )
