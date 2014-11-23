from django import forms

# class AuthenticationForm(forms.Form):
#     """
#     Login form
#     """
#     username = forms.CharField(widget=forms.widgets.TextInput)
#     password = forms.CharField(widget=forms.widgets.PasswordInput)

#     class Meta:
        # fields = ['username', 'password']

class NewBiddingForm(forms.Form):
	title = forms.CharField(max_length=255)
	description = forms.CharField(max_length=255)
	classification = forms.CharField(max_length=255)
	business_category = forms.CharField(max_length=255)
	procurement_mode = forms.CharField(max_length=255)
	budget = forms.CharField(max_length=255)
	contact_person = forms.CharField(max_length=255)
	contact_address = forms.CharField(max_length=255)
	reason = forms.CharField(max_length=255)