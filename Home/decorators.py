from django.shortcuts import redirect
from .models import Profile

def profile_completed_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.profile
            # If any required field is blank
            if not profile.full_name or not profile.class_name or not profile.section:
                return redirect('complete_profile')  # name of the profile form view
        except Profile.DoesNotExist:
            return redirect('complete_profile')
        return view_func(request, *args, **kwargs)
    return wrapper
