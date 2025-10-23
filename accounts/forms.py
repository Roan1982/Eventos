from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import UserProfile, MediaBlob
from events.models import Category, UserInterest

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    avatar_file = forms.FileField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'phone', 'bio',
            'contact_email', 'contact_whatsapp', 'contact_telegram', 'allow_contact'
        ]

    def clean_avatar_file(self):
        f = self.files.get('avatar_file')
        if not f:
            return None
        if f.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError('Archivo demasiado grande (max 10MB).')
        if f.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise ValidationError('Tipo de archivo no permitido.')
        return f

    def save(self, commit=True):
        instance = super().save(commit=False)
        f = self.cleaned_data.get('avatar_file')
        if f:
            blob = MediaBlob.objects.create(
                content=f.read(),
                content_type=f.content_type or 'application/octet-stream',
                filename=f.name,
                size=f.size,
            )
            instance.avatar = blob
        if commit:
            instance.save()
        return instance

class UserInterestForm(forms.ModelForm):
    """Formulario para gestionar los intereses del usuario"""
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categorías de Interés'
    )
    
    class Meta:
        model = UserInterest
        fields = ['categories', 'notify_new_events', 'notify_updates', 'notify_reminders']
        labels = {
            'notify_new_events': 'Notificarme cuando se publiquen nuevos eventos de mi interés',
            'notify_updates': 'Notificarme cuando se actualicen eventos que sigo',
            'notify_reminders': 'Recordatorios de eventos próximos',
        }
        widgets = {
            'notify_new_events': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_updates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
