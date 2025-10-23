from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Event, Category, Tag, MediaBlob, Review
from .forms import EventForm, ReviewForm, ContactForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured'] = Event.objects.filter(status='published', featured=True)[:6]
        ctx['latest'] = Event.objects.filter(status='published')[:6]
        return ctx

class EventListView(ListView):
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        qs = Event.objects.filter(status='published').annotate(avg_rating=Avg('reviews__rating'), review_count=Count('reviews'))
        q = self.request.GET.get('q')
        city = self.request.GET.get('city')
        category = self.request.GET.get('category')
        price = self.request.GET.get('price')  # free/paid
        order = self.request.GET.get('order')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if city:
            qs = qs.filter(city__iexact=city)
        if category:
            qs = qs.filter(category__slug=category)
        if price == 'free':
            qs = qs.filter(is_free=True)
        elif price == 'paid':
            qs = qs.filter(is_free=False)
        if order == 'popular':
            qs = qs.order_by('-review_count')
        elif order == 'featured':
            qs = qs.order_by('-featured', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs

class EventDetailView(DetailView):
    template_name = 'events/detail.html'
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['review_form'] = ReviewForm()
        ctx['contact_form'] = ContactForm()
        ctx['avg_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
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
        form.instance.creator = self.request.user
        messages.success(self.request, 'Evento creado')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, CreatorOrAdminMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar este evento')
        return redirect(self.get_object().get_absolute_url())

class EventDeleteView(LoginRequiredMixin, CreatorOrAdminMixin, DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

@login_required
def add_review(request, slug):
    event = get_object_or_404(Event, slug=slug)
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.update_or_create(
            user=request.user, event=event,
            defaults={'rating': form.cleaned_data['rating'], 'comment': form.cleaned_data['comment']}
        )
        messages.success(request, 'Reseña guardada')
    return redirect(event.get_absolute_url())

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_superuser or review.event.creator == request.user:
        review.delete()
        messages.success(request, 'Reseña eliminada')
    else:
        messages.error(request, 'No autorizado')
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
