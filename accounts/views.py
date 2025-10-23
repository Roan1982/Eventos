from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, ProfileForm
from .models import UserProfile, MediaBlob

# Simple email verification token using built-in PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator as token_generator


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require email verification
            user.save()

            current_site = get_current_site(request)
            subject = 'Verifica tu cuenta'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            verify_url = request.build_absolute_uri(reverse('accounts:verify_email', args=[uid, token]))
            message = render_to_string('accounts/verify_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'verify_url': verify_url,
            })
            send_mail(subject, message, None, [user.email])
            messages.success(request, 'Revisa tu email para verificar la cuenta.')
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
    messages.success(request, 'Cuenta verificada. Puedes iniciar sesión.')
    return redirect('accounts:login')
    messages.error(request, 'Enlace inválido o expirado.')
    return redirect('home')


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})


def blob_serve(request, pk):
    # Serve MediaBlob content with proper content-type
    blob = get_object_or_404(MediaBlob, pk=pk)
    from django.http import HttpResponse
    resp = HttpResponse(blob.content, content_type=blob.content_type)
    resp['Content-Disposition'] = f"inline; filename={blob.filename}"
    resp['Cache-Control'] = 'public, max-age=86400'
    return resp
