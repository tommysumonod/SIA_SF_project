from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Users
import uuid
from django.http import JsonResponse
from .models import Users, ProfileBio
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# ---------- PAGE VIEWS ----------
def home(request):
    return render(request, 'pages/hero.html')

def create(request):
    return render(request, 'pages/create.html')

def signin_page(request):
    return render(request, 'pages/signin.html')

def signup_page(request):
    return render(request, 'pages/signup.html')

def hero(request):
    """Main landing page"""
    return render(request, 'pages/hero.html')

def hero(request):
    user = None
    if 'user_uid' in request.session:
        try:
            user = Users.objects.get(uid=request.session['user_uid'])
        except Users.DoesNotExist:
            request.session.flush()

    return render(request, 'pages/hero.html', {'user': user})

def update_profile_bio(request):
    """AJAX endpoint to update profile bio info (address, bio only)."""
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        user = Users.objects.get(uid=request.session['user_uid'])
        profile_bio, _ = ProfileBio.objects.get_or_create(profile_uid=user)

        profile_bio.address = request.POST.get('address', profile_bio.address)
        profile_bio.bio = request.POST.get('bio', profile_bio.bio)
        profile_bio.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def profile_view(request):
    """Profile view (manual session auth)."""
    if 'user_uid' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('signin')

    user = Users.objects.get(uid=request.session['user_uid'])
    profile_bio, _ = ProfileBio.objects.get_or_create(profile_uid=user)

    context = {
        'user': user,
        'profile_bio': profile_bio,
    }
    return render(request, 'pages/profile.html', context)


def upload_profile_picture(request):
    """Handle AJAX upload for profile picture."""
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)

    if request.method == 'POST' and request.FILES.get('profile_pic'):
        user = Users.objects.get(uid=request.session['user_uid'])
        user.profile_pic = request.FILES['profile_pic']
        user.save()
        return JsonResponse({'success': True, 'image_url': user.profile_pic.url})

    return JsonResponse({'success': False, 'error': 'No file uploaded'})


def profile(request):
    """Profile page — requires login"""
    if 'user_uid' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('hero')

    user = Users.objects.get(uid=request.session['user_uid'])
    return render(request, 'pages/profile.html', {'user': user})


def gallery(request):
    return render(request, 'pages/gallery.html')


def chat(request):
    return render(request, 'pages/chat.html')


def uploads(request):
    return render(request, 'pages/uploads.html')


# ---------- AUTH: SIGNUP ----------
def signup_view(request):
    # Render signup page on GET, handle creation on POST
    if request.method == 'POST':
        email = request.POST.get('signupEmail')
        password = request.POST.get('signupPassword')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        birthdate = request.POST.get('birthdate')

        if not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('signup')

        if Users.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')
        if Users.objects.filter(firstname=firstname).exists():
            messages.error(request, "First name already exists.")
            return redirect('signup')
        if Users.objects.filter(lastname=lastname).exists():
            messages.error(request, "Last name already exists.")
            return redirect('signup')

        new_user = Users(
            uid=str(uuid.uuid4()),
            username=email.split('@')[0],
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=make_password(password),
        )
        new_user.save()

        messages.success(request, "Account created; please proceed to login.")
        return redirect('signin')

    # If GET, render signup page
    return render(request, 'pages/signup.html')


# ---------- AUTH: LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        if not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('signin')

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            messages.error(request, "Account doesn’t exist or mismatched credentials.")
            return redirect('signin')

        if check_password(password, user.password):
            request.session['user_uid'] = user.uid
            return redirect('gallery')
        else:
            messages.error(request, "Account doesn’t exist or mismatched credentials.")
            return redirect('signin')

    return redirect('hero')


# ---------- AUTH: LOGOUT ----------
def logout_view(request):
    request.session.flush()
    return redirect('hero')
