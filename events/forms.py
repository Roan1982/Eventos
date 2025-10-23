from django import forms
import datetime
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Event, Review, ContactMessage, MediaBlob, Tag

class EventForm(forms.ModelForm):
    # ClearableFileInput doesn't support multiple by default in some Django versions.
    # Create a small subclass that enables multiple selection and use it.
    class MultiClearableFileInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    media_files = forms.FileField(widget=MultiClearableFileInput(attrs={'multiple': True, 'class': 'filepond'}), required=False)

    # split date and time fields for start and end
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Event
        fields = [
            'title','description','category','price','venue_name','address','city','latitude','longitude','capacity','status','tags','featured'
        ]
        widgets = {}

    def clean_media_files(self):
        files = self.files.getlist('media_files')
        for f in files:
            if f.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError('Archivo demasiado grande (max 10MB).')
            if getattr(f, 'content_type', None) not in settings.ALLOWED_CONTENT_TYPES:
                raise ValidationError('Tipo de archivo no permitido.')
        return files

    def clean(self):
        cleaned = super().clean()
        sd = cleaned.get('start_date')
        st = cleaned.get('start_time')
        ed = cleaned.get('end_date')
        et = cleaned.get('end_time')
        if sd and st:
            cleaned['start_datetime'] = datetime.datetime.combine(sd, st)
        if ed and et:
            cleaned['end_datetime'] = datetime.datetime.combine(ed, et)
        # ensure chronology
        sdtime = cleaned.get('start_datetime')
        edtime = cleaned.get('end_datetime')
        if sdtime and edtime and sdtime > edtime:
            raise ValidationError('La fecha/hora de inicio debe ser anterior a la de fin.')
        return cleaned

    def save(self, commit=True):
        # Save model instance, then create MediaBlob entries
        instance = super().save(commit=False)
        # set computed fields if present
        sdtime = self.cleaned_data.get('start_datetime')
        edtime = self.cleaned_data.get('end_datetime')
        if sdtime:
            instance.start_datetime = sdtime
        if edtime:
            instance.end_datetime = edtime
        if commit:
            instance.save()
            # save M2M
            try:
                self.save_m2m()
            except Exception:
                pass
        else:
            # caller will save
            pass

        files = self.files.getlist('media_files')
        for f in files:
            MediaBlob.objects.create(
                event=instance,
                content=f.read(),
                content_type=getattr(f, 'content_type', 'application/octet-stream'),
                filename=f.name,
                size=getattr(f, 'size', None) or 0,
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
