from django import forms
import datetime
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Event, Review, ContactMessage, MediaBlob, Tag

class EventForm(forms.ModelForm):
    # Multi-file upload widget
    class MultiClearableFileInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    class MultiFileField(forms.FileField):
        def clean(self, data, initial=None):
            if data is None:
                return []
            if isinstance(data, list):
                cleaned = []
                for f in data:
                    cleaned.append(super().clean(f, initial))
                return cleaned
            return [super().clean(data, initial)]

    media_files = MultiFileField(
        widget=MultiClearableFileInput(attrs={'multiple': True, 'class': 'filepond', 'accept': 'image/*,video/*'}), 
        required=False,
        help_text='Arrastra archivos aquí o haz clic para seleccionar (máx 10MB por archivo)'
    )

    # Split date and time fields for better UX
    start_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='Fecha de inicio'
    )
    start_time = forms.TimeField(
        required=True, 
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        help_text='Hora de inicio'
    )
    end_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='Fecha de fin'
    )
    end_time = forms.TimeField(
        required=True, 
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        help_text='Hora de fin'
    )

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'category', 'price', 'venue_name', 'address', 
            'city', 'latitude', 'longitude', 'capacity', 'status', 'tags', 'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Concierto de Rock en Vivo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe tu evento...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'venue_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estadio Nacional'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle y número'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Buenos Aires'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Opcional'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Opcional'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '0 = ilimitado'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
        }
        help_texts = {
            'title': 'Título atractivo y descriptivo',
            'description': 'Incluye detalles importantes del evento',
            'capacity': 'Deja en 0 para capacidad ilimitada',
            'featured': 'Marcar para mostrar en página principal',
        }

    def __init__(self, *args, **kwargs):
        # If an instance is provided (editing), populate split date/time fields
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance and getattr(instance, 'pk', None):
            try:
                if instance.start_datetime:
                    # Use ISO format for date and HH:MM for time so HTML5 inputs render correctly
                    self.initial.setdefault('start_date', instance.start_datetime.date().isoformat())
                    self.initial.setdefault('start_time', instance.start_datetime.time().strftime('%H:%M'))
                if instance.end_datetime:
                    self.initial.setdefault('end_date', instance.end_datetime.date().isoformat())
                    self.initial.setdefault('end_time', instance.end_datetime.time().strftime('%H:%M'))
            except Exception:
                # be defensive; do not crash form init
                pass

    def clean_media_files(self):
        files = self.files.getlist('media_files') or self.files.getlist('media_files[]') or []
        fd = self.cleaned_data.get('media_files')
        
        # DEBUG
        print(f"DEBUG clean_media_files - self.files.keys(): {list(self.files.keys())}")
        print(f"DEBUG clean_media_files - files: {files}")
        print(f"DEBUG clean_media_files - fd: {fd}")
        
        if fd and isinstance(fd, list):
            files = fd
        # Validate each file
        for f in files:
            if getattr(f, 'size', 0) > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(f'Archivo "{getattr(f, "name", "desconocido")}" demasiado grande (máx {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB).')
            ctype = getattr(f, 'content_type', '')
            if ctype and ctype not in settings.ALLOWED_CONTENT_TYPES:
                raise ValidationError(f'Tipo de archivo "{ctype}" no permitido. Solo se permiten imágenes y videos.')
        return files

    def clean(self):
        cleaned = super().clean()
        sd = cleaned.get('start_date')
        st = cleaned.get('start_time')
        ed = cleaned.get('end_date')
        et = cleaned.get('end_time')
        
        if sd and st:
            naive_start = datetime.datetime.combine(sd, st)
            cleaned['start_datetime'] = timezone.make_aware(naive_start) if timezone.is_naive(naive_start) else naive_start
        
        if ed and et:
            naive_end = datetime.datetime.combine(ed, et)
            cleaned['end_datetime'] = timezone.make_aware(naive_end) if timezone.is_naive(naive_end) else naive_end
        
        # Validate chronology
        sdtime = cleaned.get('start_datetime')
        edtime = cleaned.get('end_datetime')
        if sdtime and edtime:
            if sdtime >= edtime:
                raise ValidationError('La fecha/hora de inicio debe ser anterior a la de fin.')
            # Warn if event is too long (more than 7 days)
            duration = (edtime - sdtime).total_seconds() / 86400
            if duration > 7:
                self.add_error(None, ValidationError(f'El evento dura {duration:.1f} días. ¿Es correcto?', code='long_duration'))
        
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

            # Prefer cleaned_data (MultiFileField normalized to a list) but
            # fall back to raw uploaded files from self.files under common keys
            files = self.cleaned_data.get('media_files') or self.files.getlist('media_files') or self.files.getlist('media_files[]') or list(self.files.values()) or []
            for f in files:
                # f may be an UploadedFile or similar; read content
                try:
                    content = f.read()
                except Exception:
                    # if content already bytes
                    content = f if isinstance(f, (bytes, bytearray)) else None
                MediaBlob.objects.create(
                    event=instance,
                    content=content or b'',
                    content_type=getattr(f, 'content_type', 'application/octet-stream'),
                    filename=getattr(f, 'name', getattr(f, 'filename', 'blob')),
                    size=getattr(f, 'size', None) or (len(content) if content else 0),
                )
        else:
            # caller will save the instance and handle blobs if desired
            pass
        return instance

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
