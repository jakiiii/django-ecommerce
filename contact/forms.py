from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control",
                                                                              "id": "fullName",
                                                                              "placeholder": "your full name"}))
    email = forms.EmailField(max_length=32, widget=forms.EmailInput(attrs={"class": "form-control",
                                                                          "id": "email",
                                                                          "placeholder": "your email"}))
    contact = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",
                                                           "id": "contact_message",
                                                           "placeholder": "your message"}))

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be Gamil.")
    #     return email

    # def clean_contact(self):
    #     raise forms.ValidationError("Your contact address is not correct!")
