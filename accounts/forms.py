
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    display_name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "display_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.display_name = self.cleaned_data["display_name"]

        if commit:
            user.save()

        return user
