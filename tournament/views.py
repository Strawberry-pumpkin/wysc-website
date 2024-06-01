from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, BooleanField, Q
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from tournament.models import Tournament, Participant

def index(request):
    frm = request.session.get('from', '')
    request.session['from'] = ''
    request.session.save()

    return render(request, 'index.html', {"from": frm})


def redirect_view(request):
    if request.path not in ['/worker.js','favicon.ico']:
        request.session['from'] = request.path or ''
    return redirect('/')



def register(request):
    if request.user.is_authenticated and request.method == "POST":
        t = Tournament.objects.get(pk=request.POST.get('tournament'))
        Participant.objects.create(
            user=request.user, tournament=t,name=request.user.profile.preferred_name,
        )

        message = EmailMultiAlternatives(subject=f"{t.name}",
                                         from_email='Scrabble Federation of Sri Lanka <wysc2024@scrabble.lk>',
                                         to=[request.user.email])
        html = render_to_string('register-confirm-email.html', {'name': request.user.profile.full_name, 'tournament': t.name})
        message.attach_alternative(html, "text/html")
        message.send()
        
        return redirect('/profile/')
            
    return render(request, 'register.html')
    