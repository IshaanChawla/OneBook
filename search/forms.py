from django import forms
from myhome.models import Address

class SearchByForm(forms.Form):
    searchBar = forms.CharField(required = False,
            max_length = 40,
            label = '',
            widget=forms.TextInput(
                attrs={'placeholder' : 'Search ...',
                }
            )
        )
    OPTION = (
        ('title','Title'),
        ('author','Author'),
        ('genre','Genre'),
    )
    searchOption = forms.ChoiceField(required = False,
        widget=forms.RadioSelect,
        choices = OPTION,
        label = ''
    )

class RadiusForm(forms.Form):
    OPTION = (
        ('5','5 Km'),
        ('10','10 Km'),
        ('15','15 Km'),
    )
    radiusOption = forms.ChoiceField(required = False,
        widget=forms.RadioSelect,
        choices = OPTION,
        label = ''
    )
    
class SelectAddressForm(forms.Form):
    def __init__(self,requestingUser,*args,**kwargs):
        super(SelectAddressForm, self).__init__(*args, **kwargs)
    
        all_entries = Address.objects.all().filter(user = requestingUser)
        add_list = []
        for obj in all_entries:
            address = obj.house_number + ' ' + obj.area + ' ' + obj.city + ' ' + obj.state
            tup = (obj.id,address)
            add_list.append(tup)
        OPTION = tuple(add_list)
            
        self.fields['addressOption'] = forms.ChoiceField(required = True,
            widget=forms.RadioSelect,
            choices = OPTION,
            label = ''
        )