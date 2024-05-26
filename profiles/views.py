"""
Views for creating, editing and viewing user profiles.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Subquery, Q
from django.utils import timezone

from profiles.forms import UserProfileForm, PaymentForm, PassportForm
from ratings.models import Unrated, WespaRating, NationalRating
from tournament.models import Tournament, Participant

@login_required
def edit(request):
    profile = request.user.profile
    
    if request.method == "GET":
        form = UserProfileForm(
            initial = {'full_name': profile.full_name,
                      'phone': profile.phone,
                      'gender': profile.gender,
                      'display_name': profile.preferred_name,
                      'date_of_birth': profile.date_of_birth,
                      'country' : profile.country
            }
        )
    else:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile.full_name = form.cleaned_data['full_name']
            profile.phone = form.cleaned_data['phone']
            profile.gender = form.cleaned_data['gender']
            profile.preferred_name = form.cleaned_data['display_name']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.country = form.cleaned_data['country']
            profile.save()

            return redirect('/profile/connect/')
    return render(request, 'profiles/names.html', {
        "form": form}) 

from django.db.models import Subquery, OuterRef

def index(request):
    """Wait till confirmation is received"""

    profile = request.user.profile
    if not profile.full_name:
        return edit(request)   
    else:
        form = PassportForm()

        tournaments = Tournament.objects.filter(
            Q(start_date__gte=timezone.now()) & Q(registration_open=True)
        )
        for t in tournaments:
            p = t.participants.filter(user=request.user)
            if p.exists():
                t.registered = p.first()
            
        return render(request, 'profiles/index.html', {'tournaments': tournaments, 'form': form})

def search_names(rtype, name):
    if rtype == "wespa":
        qs = WespaRating.objects
    elif rtype == "national":
        qs = NationalRating.objects
    else:
        qs = Unrated.objects

    return qs.annotate(
            similarity=TrigramSimilarity('name', name)
    ).filter(similarity__gt=0.75).order_by('-similarity')


@login_required
def connect(request):
    profile = request.user.profile

    if request.method == "GET":
        if not profile.full_name:
            redirect('/profile/')

        wespa = search_names("wespa", profile.preferred_name)

        
        return render(request, 'profiles/connect.html', 
                { "wespa": wespa}
        )
    
    else:
        wespa = request.POST.get('wespa')
        national = request.POST.get('national')
        unrated = request.POST.get('unrated')

        if not wespa and not national and not unrated:
            request.user.profile.beginner = True
        else:
            request.user.profile.wespa_list_name = wespa
            request.user.profile.national_list_name = national
            request.user.profile.beginner = False
        
        request.user.profile.save()
        return redirect('/profile/')


@login_required
def passport(request):
    """Upload passport image"""
    if request.method == 'POST':
        p = PassportForm(request.POST, request.FILES)
        if p.is_valid():
            participant = Participant.objects.get(tournament=p.cleaned_data['tournament'], user=request.user)
            participant.passport = p.cleaned_data['passport']
            participant.save()
            return redirect('/profile/')


@login_required
def payment(request):
    """Display payment information for a tournament.
    """
    
    participants = Participant.objects.filter(user=request.user)
    for p in participants:
        p.form = PaymentForm(initial={'tournament': p.tournament.id})

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = participants.exclude(approval='V').get(tournament=form.cleaned_data['tournament'])
            instance.payment = form.cleaned_data['payment']
            instance.approval = 'P'
            instance.save()
            return redirect('/profile/payment/')
    
    return render(request, 'profiles/payment.html', 
                    {'participants': participants}
            )
    
    