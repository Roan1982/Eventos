from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, F
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import datetime
import pytz

from .models import Event, Category, Tag, MediaBlob, Review, Favorite, UserInterest, Notification
from .forms import EventForm, ReviewForm, ContactForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Featured events with cover media prefetch
        ctx['featured'] = Event.objects.filter(
            status='published', featured=True
        ).select_related('category', 'cover_media').prefetch_related('media')[:6]
        
        # Latest events
        ctx['latest'] = Event.objects.filter(
            status='published'
        ).select_related('category', 'cover_media').prefetch_related('media')[:6]
        
        # Stats for homepage
        ctx['total_events'] = Event.objects.filter(status='published').count()
        ctx['categories'] = Category.objects.annotate(event_count=Count('event')).filter(event_count__gt=0)
        
        return ctx

class EventListView(ListView):
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        qs = Event.objects.filter(status='published').select_related(
            'category', 'creator', 'cover_media'
        ).prefetch_related('media').annotate(
            avg_rating=Avg('reviews__rating'), 
            review_count=Count('reviews')
        )
        
        # Search filters
        q = self.request.GET.get('q')
        city = self.request.GET.get('city')
        category = self.request.GET.get('category')
        price = self.request.GET.get('price')
        order = self.request.GET.get('order')
        
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(venue_name__icontains=q))
        if city:
            qs = qs.filter(city__iexact=city)
        if category:
            qs = qs.filter(category__slug=category)
        if price == 'free':
            qs = qs.filter(is_free=True)
        elif price == 'paid':
            qs = qs.filter(is_free=False)
        
        # Ordering
        if order == 'popular':
            qs = qs.order_by('-review_count', '-view_count')
        elif order == 'featured':
            qs = qs.order_by('-featured', '-created_at')
        elif order == 'price_low':
            qs = qs.order_by('price', '-created_at')
        elif order == 'price_high':
            qs = qs.order_by('-price', '-created_at')
        else:
            qs = qs.order_by('-start_datetime')
        
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['cities'] = Event.objects.filter(status='published').values_list('city', flat=True).distinct().order_by('city')
        return ctx

class EventDetailView(DetailView):
    template_name = 'events/detail.html'
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        Event.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['review_form'] = ReviewForm()
        ctx['contact_form'] = ContactForm()
        ctx['avg_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        ctx['review_count'] = self.object.reviews.count()
        
        # Check if user has favorited this event
        if self.request.user.is_authenticated:
            ctx['is_favorited'] = Favorite.objects.filter(
                user=self.request.user, 
                event=self.object
            ).exists()
        else:
            ctx['is_favorited'] = False
        
        # Provide ordered media list
        try:
            ctx['media_list'] = self.object.media.all().order_by('display_order', '-size')
        except Exception:
            ctx['media_list'] = self.object.media.all()
        # Related events
        ctx['related_events'] = Event.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(pk=self.object.pk).select_related('cover_media')[:4]
        return ctx

class CreatorOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object() if hasattr(self, 'get_object') else None
        return self.request.user.is_superuser or (obj and obj.creator == self.request.user)

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'

    def form_valid(self, form):
        # Save the instance first so we have a PK to attach MediaBlob rows to.
        form.instance.creator = self.request.user
        
        # DEBUG: ver qué archivos llegan
        print(f"DEBUG FILES: {self.request.FILES}")
        print(f"DEBUG FILES keys: {list(self.request.FILES.keys())}")
        print(f"DEBUG media_files: {self.request.FILES.getlist('media_files')}")
        
        # Let the form.save() handle saving instance, computed fields and MediaBlob rows.
        instance = form.save(commit=True)
        messages.success(self.request, 'Evento creado')
        self.object = instance
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

class EventUpdateView(LoginRequiredMixin, CreatorOrAdminMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar este evento')
        return redirect(self.get_object().get_absolute_url())
    
    def form_valid(self, form):
        # Use form.save() so EventForm.save handles datetimes and media blobs
        # If the form included deletion checkboxes, remove those media blobs first
        delete_ids = self.request.POST.getlist('delete_media')
        if delete_ids:
            # only delete blobs that belong to this event for safety
            MediaBlob.objects.filter(id__in=delete_ids, event=form.instance).delete()

        # If user selected a cover_media radio, set it (ensure it belongs to this event)
        cover_id = self.request.POST.get('cover_media')
        if cover_id:
            try:
                cover = MediaBlob.objects.get(pk=int(cover_id), event=form.instance)
                form.instance.cover_media = cover
            except Exception:
                # ignore invalid cover selection
                pass

        instance = form.save(commit=True)
        try:
            form.save_m2m()
        except Exception:
            pass
        messages.success(self.request, 'Evento actualizado')
        self.object = instance
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

class EventDeleteView(LoginRequiredMixin, CreatorOrAdminMixin, DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

@login_required
def add_review(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    # Verificar si el usuario ya tiene una reseña
    existing_review = Review.objects.filter(user=request.user, event=event).first()
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        if existing_review:
            # Actualizar reseña existente
            existing_review.rating = form.cleaned_data['rating']
            existing_review.comment = form.cleaned_data['comment']
            existing_review.save()
            messages.info(request, 'Tu reseña ha sido actualizada')
        else:
            # Crear nueva reseña
            Review.objects.create(
                user=request.user,
                event=event,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            messages.success(request, 'Reseña guardada exitosamente')
    else:
        messages.error(request, 'Error al guardar la reseña. Verifica los datos.')
    
    return redirect(event.get_absolute_url())

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    # Solo staff/superuser pueden eliminar reseñas
    if request.user.is_staff or request.user.is_superuser:
        review.delete()
        messages.success(request, 'Reseña eliminada')
    else:
        messages.error(request, 'No tienes permisos para eliminar reseñas')
    return redirect(review.event.get_absolute_url())

def media_blob_serve(request, pk):
    blob = get_object_or_404(MediaBlob, pk=pk)
    resp = HttpResponse(blob.content, content_type=blob.content_type)
    resp['Content-Disposition'] = f"inline; filename={blob.filename}"
    resp['Cache-Control'] = 'public, max-age=86400'
    return resp

@login_required
def contact_creator(request, slug):
    event = get_object_or_404(Event, slug=slug)
    form = ContactForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.event = event
        msg.save()
        messages.success(request, 'Mensaje enviado (revisa la consola de emails en dev).')
    return redirect(event.get_absolute_url())

# ===== Favorites Views =====
@login_required
def toggle_favorite(request, slug):
    """Toggle favorite status for an event"""
    event = get_object_or_404(Event, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, event=event)
    
    if not created:
        # Ya existía, entonces lo eliminamos (unfavorite)
        favorite.delete()
        messages.info(request, f'"{event.title}" eliminado de favoritos')
    else:
        # Se creó nuevo (favorite)
        messages.success(request, f'"{event.title}" agregado a favoritos ❤')
    
    # Redirect to the referrer or event detail
    return redirect(request.META.get('HTTP_REFERER', event.get_absolute_url()))

class FavoriteListView(LoginRequiredMixin, ListView):
    """Lista de eventos favoritos del usuario"""
    model = Favorite
    template_name = 'events/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            'event__category', 'event__cover_media'
        ).prefetch_related('event__media')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['favorite_count'] = self.get_queryset().count()
        return ctx

# ===== Calendar Export =====
def event_to_ics(request, slug):
    """Generar archivo .ics para agregar evento al calendario"""
    event = get_object_or_404(Event, slug=slug)
    
    # Formatear fechas al formato iCalendar (YYYYMMDDTHHMMSS)
    def format_datetime(dt):
        """Convierte datetime a formato iCalendar"""
        if dt.tzinfo is None:
            # Si no tiene timezone, asumimos UTC
            dt = pytz.UTC.localize(dt)
        return dt.strftime('%Y%m%dT%H%M%SZ')
    
    # Construir el contenido del archivo .ics
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ReJuntada//Eventos//ES
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{event.id}@rejuntada.com
DTSTAMP:{format_datetime(datetime.now(pytz.UTC))}
DTSTART:{format_datetime(event.start_datetime)}
DTEND:{format_datetime(event.end_datetime if event.end_datetime else event.start_datetime)}
SUMMARY:{event.title}
DESCRIPTION:{event.description[:500]}
LOCATION:{event.venue_name or ''}{', ' + event.address if event.address else ''}, {event.city}
URL:{request.build_absolute_uri(event.get_absolute_url())}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR"""
    
    # Crear la respuesta HTTP
    response = HttpResponse(ics_content, content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{event.slug}.ics"'
    return response

# ===== Admin Dashboard =====
@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    """Dashboard administrativo con estadísticas y reportes"""
    template_name = 'events/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        
        # Estadísticas generales
        ctx['total_events'] = Event.objects.count()
        ctx['published_events'] = Event.objects.filter(status='published').count()
        ctx['pending_events'] = Event.objects.filter(status='draft').count()
        ctx['total_users'] = User.objects.count()
        ctx['total_reviews'] = Review.objects.count()
        ctx['total_favorites'] = Favorite.objects.count()
        ctx['total_notifications'] = Notification.objects.count()
        ctx['unread_notifications'] = Notification.objects.filter(is_read=False).count()
        
        # Promedio de rating
        ctx['avg_rating'] = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Eventos recientes (últimos 10)
        ctx['recent_events'] = Event.objects.select_related(
            'creator', 'category'
        ).order_by('-created_at')[:10]
        
        # Eventos próximos
        now = timezone.now()
        ctx['upcoming_events'] = Event.objects.filter(
            status='published',
            start_datetime__gte=now
        ).select_related('category').order_by('start_datetime')[:10]
        
        # Top categorías por número de eventos
        ctx['top_categories'] = Category.objects.annotate(
            event_count=Count('event')
        ).filter(event_count__gt=0).order_by('-event_count')[:10]
        
        # Top eventos por vistas
        ctx['top_viewed_events'] = Event.objects.filter(
            status='published'
        ).order_by('-view_count')[:10]
        
        # Reseñas recientes
        ctx['recent_reviews'] = Review.objects.select_related(
            'user', 'event'
        ).order_by('-created_at')[:10]
        
        # Estadísticas de la última semana
        week_ago = now - timedelta(days=7)
        ctx['events_this_week'] = Event.objects.filter(created_at__gte=week_ago).count()
        ctx['reviews_this_week'] = Review.objects.filter(created_at__gte=week_ago).count()
        ctx['users_this_week'] = User.objects.filter(date_joined__gte=week_ago).count()
        
        return ctx
