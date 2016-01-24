from .models import CustomUser
from django import forms 

class LogInForm(forms.Form):
    email = forms.EmailField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Email'}
            )
    )
    password = forms.CharField(label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Password'}
            )
    )


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Full Name'}
            )
    )
    email = forms.EmailField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Email'}
            )
    )
    password = forms.CharField(label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Password'}
            )
    )
    confpass = forms.CharField(label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Confirm Password'}
            )
    )
    
    class Meta:
        model = CustomUser
        fields = ['full_name','email','password']
        
    def clean_email(self):
        dom_arr = ['gmail','outlook','yahoo','rediff','hotmail']
        email = self.cleaned_data.get('email')
        base,provider = email.split('@')
        domain,extension = provider.split('.')
        i = 0
        while i<len(dom_arr):
            if dom_arr[i] == domain:
                break
            i += 1
        if(i == len(dom_arr)):
            raise forms.ValidationError('Please Enter a Valid Domain Name')
        if extension != 'com':
            raise forms.ValidationError('Please Enter a Valid Extension')
        
        try:
            CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist:
            return email
                
        raise forms.ValidationError('User with the Email Exists')
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 8:
            cap = 0
            small = 0
            num = 0
            for i in range(len(password)):
                if password[i]>='a' and password[i]<='z':
                    small += 1
                elif password[i]>='A' and password[i]<='Z':
                    cap += 1
                elif password[i]>='0' and password[i]<='9':
                    num += 1
            if not (cap > 0 and small > 0 and num > 0):
                raise forms.ValidationError('Password Expression not Valid')
        else:
            raise forms.ValidationError('Password Length Not Sufficient')
        return password
    
    def clean_confpass(self):
        conf_pass = self.cleaned_data.get('confpass')
        password = self.cleaned_data.get('password')
        if (password != None):
            if (password != conf_pass):
                raise forms.ValidationError('Passwords Dont Match')
            return conf_pass
        else:
            return ''
            
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user