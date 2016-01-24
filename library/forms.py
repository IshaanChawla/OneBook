from django import forms

class UserBookForm(forms.Form):
    CHOICES = [
        ('te', 'Temporary Exchange'),
        ('pe', 'Permanent Exchange'),
        ('rt', 'Rental'),
        ('sl', 'Sale')
    ]
    health = forms.DecimalField(label='',
        required = True,
        widget=forms.TextInput(
            attrs={'placeholder':'Health'}
        )
    )
    
    moe = forms.ChoiceField(required=True,
        choices = CHOICES,
        label = ''
    )
    
    ebook = forms.FileField(
        label = 'Ebook',
        required = False
    )
    
    def clean_health(self):
        health = self.cleaned_data.get('health')
        if int(health) >= 0 and int(health) <= 5:
            return health
        raise forms.ValidationError('Health Not In Range')