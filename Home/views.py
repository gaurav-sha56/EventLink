from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm
from django.contrib import messages


def index(request):
    # if request.user.is_anonymous:
    #     return redirect('/login')
    return render(request, "home.html")


    
def register(request):
    return render(request, "register.html")


def logoutUser(request):
    logout(request)
    return redirect("index")

def home(request):
    return redirect("index")

def teams(request):
    pass

def events(request):
    pass

def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        
    
        user = authenticate(username=username, password=password)
        print(username, password)
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

            if password2!=password2:
                message = "Please check both password"
            else:
                message = "User created successfully"
                user = User.objects.create_user(username, email, password1)
                login(request, user)
                print(username, password1, password2)

                return redirect('/')
            return render(request, "student_register.html", {"messages":message})
    except Exception:
        return render(request, "student_register.html")

    return render(request, "student_register.html")




def student_form(request):
    return render(request, "student_form.html")

def dashboard(request):
    return render(request, "dashboard.html")

def profile(request):
    return HttpResponse("this is profile")

def find_teammates(request):
    pass

def create_team(request):
    pass


# added today


def complete_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()  # Save the many-to-many data
            return redirect('dashboard')  # After saving, redirect to dashboard or homepage
    else:
        form = ProfileForm()
    return render(request, 'complete_profile.html', {'form': form})
