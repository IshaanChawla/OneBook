from django import forms
from booksdb.models import Genres
from .models import Address
from home.models import CustomUser

class ProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(
        label = '',
        required = False
    )
    SEX = (
        ('male','Male'),
        ('female','Female'),
    )
    sex = forms.ChoiceField(required=True,
        widget=forms.RadioSelect, 
        choices = SEX,
        label = ''
    ) 
    phone_no = forms.RegexField(label='',
        required=True,
        regex=r'^[7-9]{1}[0-9]{9}$',
        widget=forms.TextInput(
            attrs={'placeholder':'Mobile Number'}
        )
    )
    
    class Meta:
        model = CustomUser
        fields = ['profile_pic','sex','phone_no']

class AddressForm(forms.ModelForm):
    house_number = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'House/Appt Number'}
        )
    )
    area = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Area or Street'}
        )
    )
    city = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'City'}
        )
    )
    state = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'State'}
        )
    )
    zip_code = forms.RegexField(label='',
        required=True,
        regex=r'^[0-9]{6}$',
        widget=forms.TextInput(
            attrs={'placeholder':'Zip Code'}
        )
    )
    
    class Meta:
        model = Address
        fields = ['house_number','area','city','state','zip_code']
        
class InterestForm(forms.Form):
    all_entries = Genres.objects.all()
    int_list = []
    for obj in all_entries:
        tup = (obj.genre_id,obj.genre_name)
        int_list.append(tup)
    int_gen = tuple(int_list)
    interested_genres = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, 
        choices = int_gen,
        label = ''
    )
    
class BasicProfileForm(forms.Form):
    email = forms.EmailField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Email'}
            )
    )
    full_name = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Full Name'}
            )
    )

class BookListForm(forms.Form):
    book = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Book'}
            )
    )
    author = forms.CharField(label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Author'}
            )
    ) 