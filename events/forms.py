from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Event, Review, ContactMessage, MediaBlob, Tag

class EventForm(forms.ModelForm):
    # ClearableFileInput doesn't support multiple by default in some Django versions.
    # Create a small subclass that enables multiple selection and use it.
    class MultiClearableFileInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    media_files = forms.FileField(widget=MultiClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Event
        fields = [
            'title','description','category','start_datetime','end_datetime','price','venue_name','address','city','latitude','longitude','capacity','status','tags','featured'
        ]
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_media_files(self):
        files = self.files.getlist('media_files')
        for f in files:
            if f.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError('Archivo demasiado grande (max 10MB).')
            if getattr(f, 'content_type', None) not in settings.ALLOWED_CONTENT_TYPES:
                raise ValidationError('Tipo de archivo no permitido.')
        return files

    def save(self, commit=True):
        instance = super().save(commit)
        files = self.cleaned_data.get('clean_media_files', None)
        files = self.files.getlist('media_files')
        for f in files:
            MediaBlob.objects.create(
                event=instance,
                content=f.read(),
                content_type=f.content_type or 'application/octet-stream',
                filename=f.name,
                size=f.size,
            )
        return instance

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
