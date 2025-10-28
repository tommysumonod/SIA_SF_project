from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
import os
from django.db.models import Q, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Import models
from .models import Users, ProfileBio, Arts, Chats, Comments


# ---------------- HERO / LANDING ---------------- #
def hero(request):
    """Landing page — shows user if logged in."""
    user = None
    if 'user_uid' in request.session:
        user = Users.objects.filter(uid=request.session['user_uid']).first()
    return render(request, 'pages/hero.html', {'user': user})


# ---------------- MAIN PAGES ---------------- #
def gallery(request):
    return render(request, 'pages/gallery.html')


def create(request):
    """Upload form page."""
    categories = [c[0] for c in Arts.CATEGORY_CHOICES]
    return render(request, 'pages/create.html', {'categories': categories})


def signin_page(request):
    return render(request, 'pages/signin.html')


def signup_page(request):
    return render(request, 'pages/signup.html')


def chat(request):
    """General chat list page."""
    return render(request, 'pages/chat.html')


# ---------------- PROFILE ---------------- #
def profile(request):
    """View your own profile."""
    if 'user_uid' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('signin')

    user = get_object_or_404(Users, uid=request.session['user_uid'])
    profile_bio, _ = ProfileBio.objects.get_or_create(profile_uid=user)
    arts = Arts.objects.filter(uid=user)

    context = {
        'profile_user': user,
        'profile_bio': profile_bio,
        'arts': arts,
        'is_owner': True,
    }
    return render(request, 'pages/profile.html', context)

def view_profile(request, uid):
    """Render SPA that shows the selected user's profile."""
    profile_user = get_object_or_404(Users, uid=uid)
    is_owner = request.session.get('user_uid') == str(profile_user.uid)
    profile_bio = ProfileBio.objects.filter(profile_uid=profile_user).first()
    arts = Arts.objects.filter(uid=profile_user).order_by('-created_at')

    context = {
        "profile_user": profile_user,
        "profile_bio": profile_bio,
        "arts": arts,
        "is_owner": is_owner,
    }
    return render(request, "pages/profile.html", context)



@require_POST
def update_profile_bio(request):
    """Update profile bio info (address, bio)."""
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)

    user = Users.objects.get(uid=request.session['user_uid'])
    profile_bio, _ = ProfileBio.objects.get_or_create(profile_uid=user)

    profile_bio.address = request.POST.get('address', profile_bio.address)
    profile_bio.bio = request.POST.get('bio', profile_bio.bio)
    profile_bio.save()

    return JsonResponse({'success': True})


@require_POST
def upload_profile_picture(request):
    """Upload or update profile picture."""
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)

    if request.FILES.get('profile_pic'):
        user = Users.objects.get(uid=request.session['user_uid'])
        user.profile_pic = request.FILES['profile_pic']
        user.save()
        return JsonResponse({'success': True, 'image_url': user.profile_pic.url})

    return JsonResponse({'success': False, 'error': 'No file uploaded'})


# ---------------- UPLOADS ---------------- #
def all_uploads(request):
    """Show all uploads from all users."""
    arts = Arts.objects.all().order_by('-created_at')

    user = None
    if 'user_uid' in request.session:
        user = Users.objects.filter(uid=request.session['user_uid']).first()

    return render(request, 'pages/uploads.html', {
        'arts': arts,
        'user': user,
        'page_title': 'All Uploads'
    })

def search_artworks(request):
    """Search artworks by title or category and show results in uploads.html."""
    query = request.GET.get('q', '').strip()
    arts = []

    if query:
        arts = Arts.objects.filter(
            Q(title__icontains=query) | Q(category__iexact=query)
        ).order_by('-created_at')

    user = None
    if 'user_uid' in request.session:
        user = Users.objects.filter(uid=request.session['user_uid']).first()

    context = {
        'arts': arts,
        'query': query,
        'user': user,
        'page_title': f"Search results for '{query}'" if query else "Search",
    }
    return render(request, 'pages/uploads.html', context)

def uploads(request):
    """Show all uploads from all users."""
    arts = Arts.objects.all().order_by('-created_at')
    return render(request, 'pages/uploads.html', {'arts': arts, 'page_title': 'All Uploads'})


def upload_view(request, art_id):
    art = get_object_or_404(Arts, art_id=art_id)
    uploader = art.uid
    comments = Comments.objects.filter(art=art).order_by('created_at')

    can_edit = 'user_uid' in request.session and request.session['user_uid'] == uploader.uid

    return render(request, 'pages/upload-view.html', {
        'art': art,
        'uploader': uploader,
        'comments': comments,
        'can_edit': can_edit,
        'user': Users.objects.filter(uid=request.session.get('user_uid')).first(),
    })



@require_POST
def upload_art(request):
    """Handle art upload form submission."""
    if 'user_uid' not in request.session:
        messages.error(request, 'Please log in to upload.')
        return redirect('signin')

    user = Users.objects.get(uid=request.session['user_uid'])
    title = request.POST.get('title')
    description = request.POST.get('description', '')
    category = request.POST.get('category')
    image = request.FILES.get('image')

    if not title or not image:
        messages.error(request, 'Title and image are required.')
        return redirect('create')

    art_id = str(uuid.uuid4())
    image_name = default_storage.save(os.path.join('uploads', image.name), image)
    image_url = os.path.join(settings.MEDIA_URL, image_name)

    new_art = Arts.objects.create(
        art_id=art_id,
        uid=user,
        title=title,
        description=description,
        image_url=image_url,
        category=category
    )

    messages.success(request, 'Art uploaded successfully!')
    return redirect('/profile/#user-uploads')


@require_POST
def post_comment(request, art_id):
    """Post a comment on an art."""
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)

    art = get_object_or_404(Arts, art_id=art_id)
    user = Users.objects.get(uid=request.session['user_uid'])
    text = request.POST.get('comment', '').strip()

    if not text:
        return JsonResponse({'success': False, 'error': 'Empty comment'}, status=400)

    comment = Comments.objects.create(
        comment_id=str(uuid.uuid4()),
        art=art,
        uid=user,
        comment_text=text
    )

    return JsonResponse({
        'success': True,
        'comment': text,
        'user_uid': user.uid,
        'profile_pic': user.profile_pic_url,
        'name': f"{user.firstname} {user.lastname}"
    })


@require_POST
def edit_art(request, art_id):
    """Edit uploaded art."""
    art = get_object_or_404(Arts, art_id=art_id)

    if 'user_uid' not in request.session or request.session['user_uid'] != art.uid.uid:
        messages.error(request, 'Unauthorized.')
        return redirect('gallery')

    art.title = request.POST.get('title', art.title)
    art.description = request.POST.get('description', art.description)
    art.category = request.POST.get('category', art.category)
    art.save()

    messages.success(request, 'Art updated successfully!')
    return redirect('upload_view', art_id=art.art_id)

@require_POST
def delete_art(request, art_id):
    """Delete uploaded art (only by owner)."""
    art = get_object_or_404(Arts, art_id=art_id)

    # Ensure the user owns this art
    if 'user_uid' not in request.session or request.session['user_uid'] != art.uid.uid:
        messages.error(request, 'Unauthorized.')
        return redirect('gallery')

    # Delete the image file (optional but nice to have)
    if art.image_url and art.image_url.startswith(settings.MEDIA_URL):
        image_path = art.image_url.replace(settings.MEDIA_URL, '')
        if default_storage.exists(image_path):
            default_storage.delete(image_path)

    art.delete()
    messages.success(request, 'Artwork deleted successfully!')
    return redirect('profile')



def category_view(request, category_name):
    """Filter uploads by category."""
    category_name = category_name.strip()
    arts = Arts.objects.filter(category__iexact=category_name)

    user = Users.objects.filter(uid=request.session.get('user_uid')).first()

    context = {
        'arts': arts,
        'category_name': category_name,
        'user': user,
    }
    return render(request, 'pages/uploads.html', context)


# ---------------- AUTH ---------------- #
def signup_view(request):
    """Handle user signup."""
    if request.method == 'POST':
        email = request.POST.get('signupEmail')
        password = request.POST.get('signupPassword')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        if not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('signup')

        if Users.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        new_user = Users.objects.create(
            uid=str(uuid.uuid4()),
            username=email.split('@')[0],
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=make_password(password),
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('signin')

    return render(request, 'pages/signup.html')


def login_view(request):
    """Handle login."""
    if request.method == 'POST':
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect('signin')

        if check_password(password, user.password):
            request.session['user_uid'] = user.uid
            return redirect('gallery')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('signin')

    return redirect('hero')


def logout_view(request):
    """Log out and clear session."""
    request.session.flush()
    return redirect('hero')

#-----------------upload profile pic -----------------#

@require_POST
def update_profile_pic(request):
    """Handle uploading or updating user's profile picture."""
    if "user_uid" not in request.session:
        return JsonResponse({"success": False, "error": "Not logged in"}, status=401)

    user = get_object_or_404(Users, uid=request.session["user_uid"])

    if "profile_pic" in request.FILES:
        # Save the uploaded image
        user.profile_pic = request.FILES["profile_pic"]
        user.save()
        return JsonResponse({
            "success": True,
            "profile_pic_url": user.profile_pic.url
        })

    return JsonResponse({"success": False, "error": "No image provided"})



# ---------------- CHAT ---------------- #
def chat_home(request):
    if 'user_uid' not in request.session:
        return redirect('login')
    current_user = get_object_or_404(Users, uid=request.session['user_uid'])

    convo_users = get_unique_conversations(current_user)

    context = {
        'user': current_user,
        'conversations': convo_users,
        'target_user': None,
        'messages': None,
        'selected_user': None,
    }
    return render(request, 'pages/chat.html', context)



def chat_with_user(request, uid):
    if 'user_uid' not in request.session:
        return redirect('login')

    current_user = get_object_or_404(Users, uid=request.session['user_uid'])
    target_user = get_object_or_404(Users, uid=uid)

    messages = Chats.objects.filter(
        Q(sender_uid=current_user, receiver_uid=target_user) |
        Q(sender_uid=target_user, receiver_uid=current_user)
    ).order_by('created_at')

    convo_users = get_unique_conversations(current_user)

    context = {
        'user': current_user,
        'conversations': convo_users,
        'target_user': target_user,
        'messages': messages,
        'selected_user': target_user,
    }
    return render(request, 'pages/chat.html', context)



@require_POST
def send_message(request, uid):
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    sender = get_object_or_404(Users, uid=request.session['user_uid'])
    receiver = get_object_or_404(Users, uid=uid)
    text = request.POST.get('message', '').strip()

    if not text:
        return JsonResponse({'success': False, 'error': 'Empty message'}, status=400)

    chat = Chats.objects.create(
        chat_id=str(uuid.uuid4()),
        sender_uid=sender,
        receiver_uid=receiver,
        message=text,
        created_at=timezone.now(),
    )

    return JsonResponse({
        'success': True,
        'message': chat.message,
        'sender_uid': sender.uid,
        'timestamp': chat.created_at.strftime("%H:%M"),
        'sender_name': f"{sender.firstname} {sender.lastname}",
        'sender_pic': sender.profile_pic_url,
    })


def fetch_messages(request, uid):
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    current_user = get_object_or_404(Users, uid=request.session['user_uid'])
    target_user = get_object_or_404(Users, uid=uid)

    messages_qs = Chats.objects.filter(
        (Q(sender_uid=current_user, receiver_uid=target_user)) |
        (Q(sender_uid=target_user, receiver_uid=current_user))
    ).order_by('created_at')

    data = [{
        'sender_uid': m.sender_uid.uid,
        'sender_name': f"{m.sender_uid.firstname} {m.sender_uid.lastname}",
        'sender_pic': m.sender_uid.profile_pic_url,
        'message': m.message,
        'timestamp': m.created_at.strftime("%H:%M"),
    } for m in messages_qs]

    return JsonResponse({'success': True, 'messages': data})

def get_unique_conversations(current_user):
    # Get all chats involving current user
    chats = Chats.objects.filter(
        Q(sender_uid=current_user) | Q(receiver_uid=current_user)
    ).order_by('-created_at')

    unique_pairs = set()
    convo_users = []

    for chat in chats:
        # Create a normalized tuple for pair comparison (A,B same as B,A)
        pair = tuple(sorted([chat.sender_uid.uid, chat.receiver_uid.uid]))

        if pair in unique_pairs:
            continue  # Skip duplicate pairs
        unique_pairs.add(pair)

        other_user = chat.receiver_uid if chat.sender_uid == current_user else chat.sender_uid
        last_message = Chats.objects.filter(
            Q(sender_uid=current_user, receiver_uid=other_user) |
            Q(sender_uid=other_user, receiver_uid=current_user)
        ).order_by('-created_at').first()

        convo_users.append({
            'other_user': other_user,
            'last_message': last_message.message if last_message else "",
            'unread_count': 0,
        })

    return convo_users