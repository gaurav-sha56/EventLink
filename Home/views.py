from django.shortcuts import render, redirect, HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, TeamRegistrationForm
from django.contrib import messages
from .models import Team, TeamRequest, Profile, Event, TeamJoinRequest
from django.contrib.auth.decorators import login_required
from .decorators import profile_completed_required

def index(request):
    return render(request, "home.html")

def register(request):
    return render(request, "register.html")

def logoutUser(request):
    logout(request)
    return redirect("index")

def home(request):
    return redirect("index")

def teams(request):
    teams = Team.objects.all()
    return render(request, "teams.html", {"teams": teams})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_msg = "User not found ! Check id or password"
            return render(request, "student_login.html", {'error_msg':error_msg})
    return render(request, "student_login.html")

def college_login(request):
    return render(request, "college_login.html")

def college_register(request):
    pass

def student_register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                message = "Please check both password"
            else:
                message = "User created successfully"
                user = User.objects.create_user(username, email, password1)
                login(request, user)
                return redirect('/')
            return render(request, "student_register.html", {"messages": message})
    except Exception:
        return render(request, "student_register.html")

    return render(request, "student_register.html")


@profile_completed_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def find_teammates(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    teams = Team.objects.all()
    return render(request, "find_teammates.html", {"teams": teams})

@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            team = Team.objects.create(name=name, description=description, leader=request.user)
            messages.success(request, "Team created successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fill all fields")
    return render(request, 'create_team.html')

@login_required
def complete_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = ProfileForm()
    return render(request, 'complete_profile.html', {'form': form})

@login_required
def send_request(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    TeamRequest.objects.get_or_create(sender=request.user, team=team)
    return redirect('dashboard')

@login_required
def team_requests(request):
    teams = Team.objects.filter(leader=request.user)
    requests = TeamRequest.objects.filter(team__in=teams, status='pending')
    return redirect('dashboard') 

@login_required
def update_request(request, request_id, action):
    team_request = get_object_or_404(TeamRequest, id=request_id)
    if team_request.team.leader == request.user:
        if action == 'accept':
            team_request.status = 'accepted'
        elif action == 'reject':
            team_request.status = 'rejected'
        team_request.save()
    return redirect('team_requests')

@login_required
def dashboard(request):
    teams = Team.objects.all()
    received_requests = TeamRequest.objects.filter(team__leader=request.user, status='pending')
    sent_requests = TeamRequest.objects.filter(sender=request.user)
    return render(request, 'dashboard2.html', {
        'teams': teams,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    })

@login_required
def cancel_request(request, request_id):
    team_request = get_object_or_404(TeamRequest, id=request_id, sender=request.user)
    if request.method == 'POST':
        team_request.delete()
    return redirect('dashboard')


@login_required

@login_required
def register_team(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.leader = request.user
            team.event = event
            team.save()
            team.members.add(request.user)  # Optionally add leader as member
            return redirect('event_detail', event_id=event.id)
    else:
        form = TeamRegistrationForm()

    return render(request, 'register_team.html', {'form': form, 'event': event})



@login_required
def accept_request(request, request_id):
    join_request = get_object_or_404(TeamJoinRequest, id=request_id)

    if join_request.team.leader != request.user:
        messages.error(request, "You are not authorized to accept this request.")
        return redirect('dashboard')  # Redirect to a safe page

    join_request.is_approved = True
    join_request.save()
    join_request.team.members.add(join_request.user)
    messages.success(request, f"Accepted {join_request.user.username}'s request.")
    return redirect('dashboard', team_id=join_request.team.id)


@login_required
def reject_request(request, request_id):
    join_request = get_object_or_404(TeamJoinRequest, id=request_id)

    if join_request.team.leader != request.user:
        messages.error(request, "You are not authorized to reject this request.")
        return redirect('dashboard')

    join_request.is_approved = False
    join_request.save()
    messages.info(request, f"Rejected {join_request.user.username}'s request.")
    return redirect('dashboard', team_id=join_request.team.id)

def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'view_profile.html', {'profile': profile})