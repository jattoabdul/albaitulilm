from django import forms
from bookstore.models import *


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('author', 'email', 'text',)


# our contact form
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

