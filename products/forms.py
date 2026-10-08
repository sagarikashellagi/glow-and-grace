"""
Forms for Glow & Grace.

Two user-facing forms:

  ContactForm       – name, email, subject, message → ContactMessage row
  NewsletterForm    – email → NewsletterSubscriber row (unique)

Both are ModelForms so validation and saving are handled by Django.
Widget classes are set here so the HTML can use {{ form.field }} and
still come out Bootstrap-styled without manual class attributes.
"""
from django import forms

from .models import ContactMessage, NewsletterSubscriber


# ---------------------------------------------------------------------------
# Contact form
# ---------------------------------------------------------------------------
class ContactForm(forms.ModelForm):
    """
    Small contact form. All fields are required.
    The honeypot field ('website') is a lightweight anti-spam trap —
    real users leave it blank; bots fill it in.
    """
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "tabindex": "-1",
            "style": "position:absolute;left:-9999px;",
            "aria-hidden": "true",
        }),
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Your name",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "How can we help?",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control form-control-lg",
                "rows": 6,
                "placeholder": "Tell us a little more…",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "").strip()
        if len(subject) < 3:
            raise forms.ValidationError("Subject must be at least 3 characters.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Please write at least 10 characters so we can help properly."
            )
        return message

    def clean(self):
        cleaned = super().clean()
        # Honeypot trap — if the hidden field has content, reject silently
        if cleaned.get("website"):
            raise forms.ValidationError("Submission rejected.")
        return cleaned


# ---------------------------------------------------------------------------
# Newsletter form
# ---------------------------------------------------------------------------
class NewsletterForm(forms.ModelForm):
    """
    Newsletter signup. Email must be unique and case-insensitive.
    Rendered inline on the homepage and footer.
    """
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
                "required": True,
                "autocomplete": "email",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email:
            raise forms.ValidationError("Please enter your email address.")
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "You're already on the list — thank you!"
            )
        return email