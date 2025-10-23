from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('cancelled', 'Cancelado'),
    ]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200, help_text='Título del evento')
    description = models.TextField(help_text='Descripción detallada')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Precio en tu moneda local')
    is_free = models.BooleanField(default=False)
    venue_name = models.CharField(max_length=200, help_text='Nombre del lugar')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text='Capacidad máxima de asistentes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='events')
    featured = models.BooleanField(default=False, db_index=True, help_text='Mostrar en destacados')
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    cover_media = models.ForeignKey('MediaBlob', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    view_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-start_datetime']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
            models.Index(fields=['featured', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        self.is_free = (self.price == 0)
        super().save(*args, **kwargs)

class MediaBlob(models.Model):
    # Binary media storage related to events
    content = models.BinaryField()
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    display_order = models.IntegerField(default=0, help_text='Orden de visualización (menor = primero)')
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media')

    class Meta:
        ordering = ['display_order', '-size']

    def __str__(self):
        return f"{self.filename} ({self.content_type})"

    @property
    def mime_main(self):
        """Return the top-level MIME type (e.g. 'image' for 'image/png')."""
        try:
            return (self.content_type or '').split('/')[0]
        except Exception:
            return ''

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event} - {self.rating}"

class ContactMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje para {self.event.title} de {self.name}"
