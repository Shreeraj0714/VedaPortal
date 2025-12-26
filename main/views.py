from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.cache import cache

# ✅ IMPORTED PYQPaper HERE
from .models import (
    Profile, Product, Subject, Unit, Topic, Question,
    RevisionMaterial, MockPaper, PYQPaper, ContentViolation
)
from .utils import premium_required

# =====================================================
# 1. NEW: DYNAMIC CONTENT & READER MODE
# =====================================================

def subject_view(request, subject_name):
    subject = get_object_or_404(Subject, name=subject_name)
    return render(request, 'subject_content.html', {'subject': subject})

def topic_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    next_topic = Topic.objects.filter(
        unit=topic.unit, order__gt=topic.order
    ).order_by('order').first()

    if not next_topic:
        next_unit = Unit.objects.filter(
            subject=topic.unit.subject,
            order__gt=topic.unit.order
        ).order_by('order').first()
        if next_unit:
            next_topic = next_unit.topics.order_by('order').first()

    return render(request, 'topic_reader.html', {
        'topic': topic,
        'next_topic': next_topic
    })


# =====================================================
# 2. LANDING & COLLEGE SELECTION
# =====================================================

def landing(request):
    return render(request, 'landing.html')

def college_our(request):
    request.session['college_name'] = 'D.Y. Patil College of Eng & Tech'
    request.session['college_code'] = 'DYPCET'
    return redirect('login')

def college_wip(request):
    return render(request, 'college_wip.html')


# =====================================================
# 3. AUTHENTICATION
# =====================================================

@login_required
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        unique_id = request.POST.get('unique_id')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=unique_id).exists():
            messages.error(request, "Unique ID already registered")
            return redirect('register')

        # 1. Create the User
        # NOTE: The post_save Signal in models.py automatically creates the Profile.
        new_user = User.objects.create_user(
            username=unique_id,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):
    if request.method == "POST":
        # Updated to match 'unique_id' from your HTML form
        unique_id = request.POST.get('unique_id')
        password = request.POST.get('password')

        user = authenticate(request, username=unique_id, password=password)

        if user:
            login(request, user)
            
            # Support for 'next' parameter to return user to their last page
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')

        messages.error(request, "Invalid Unique ID or Password")
        return redirect('login')

    return render(request, 'login.html')

def check_session(request):
    """
    Heartbeat view to check if the session is still valid.
    Used for instant logout detection.
    """
    if request.user.is_authenticated:
        current_session_key = request.session.session_key
        stored_session_key = cache.get(f'user_session_{request.user.id}')
        
        if stored_session_key and current_session_key != stored_session_key:
            return JsonResponse({'valid': False})
        return JsonResponse({'valid': True})
    return JsonResponse({'valid': False})

def logout_user(request):
    logout(request)
    return redirect('login')


# =====================================================
# 4. PAYMENT & PREMIUM
# =====================================================

@login_required
def payment(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    new_item_request = request.GET.get('item')

    if profile.payment_status == 'pending' and not new_item_request:
        return render(request, 'payment.html', {'profile': profile})

    if request.method == 'POST':
        item_name = request.POST.get('payment_name')
        holder_name = request.POST.get('holder_name')
        mobile = request.POST.get('mobile_number')
        utr_ref = request.POST.get('payment_ref')

        combined_ref = f"UTR: {utr_ref} | Name: {holder_name} | Mob: {mobile}"

        profile.payment_name = item_name
        profile.payment_ref = combined_ref
        profile.payment_status = 'pending'
        profile.save()

        messages.success(request, "Request Sent! Please wait for approval.")
        return redirect('payment')

    return render(request, 'payment.html', {'profile': profile})

@premium_required
def premium_content(request):
    return render(request, 'premium.html')


# =====================================================
# 5. ACADEMIC STRUCTURE & ACCESS
# =====================================================

def semester_subjects(request, semester):
    return render(request, 'semester.html', {
        'semester': semester.replace('-', ' ').title()
    })

def subject_units(request, semester, branch, subject):
    user_products = []
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_products = list(
            request.user.profile.unlocked_products.values_list('slug', flat=True)
        )

    branch_bundle_key = f"{branch}-full-bundle"
    subject_bundle_key = f"{subject}-bundle"

    has_qb = (f"{subject}-qb" in user_products) or subject_bundle_key in user_products or branch_bundle_key in user_products
    has_paper = (f"{subject}-paper" in user_products) or subject_bundle_key in user_products or branch_bundle_key in user_products
    has_revision = (f"{subject}-rev" in user_products) or subject_bundle_key in user_products or branch_bundle_key in user_products
    has_pyq = subject_bundle_key in user_products or branch_bundle_key in user_products

    return render(request, 'subject_units.html', {
        'semester': semester,
        'branch': branch,
        'subject': subject,
        'has_qb': has_qb,
        'has_paper': has_paper,
        'has_revision': has_revision,
        'has_pyq': has_pyq
    })


# =====================================================
# 6. SYLLABUS VIEW
# =====================================================

def subject_syllabus(request, semester, branch, subject):
    formatted_name = subject.replace('-', ' ').title()
    db_subject = Subject.objects.filter(name__iexact=formatted_name).first()

    units = []
    using_db = False

    if db_subject:
        units = db_subject.units.all()
        using_db = True

    return render(request, 'subject_syllabus.html', {
        'semester': semester,
        'branch': branch,
        'subject': subject,
        'units': units,
        'using_db': using_db
    })


# =====================================================
# 7. PACKAGES
# =====================================================

@login_required
def packages(request):
    return render(request, 'packages.html')


# =====================================================
# 8. EXAM CONTENT VIEWS
# =====================================================

def question_bank_view(request, subject_name):
    subject = get_object_or_404(Subject, name__iexact=subject_name.replace('-', ' ').title())
    questions = Question.objects.filter(subject=subject).order_by('-probability')
    return render(request, 'question_bank.html', {'subject': subject, 'questions': questions})

def revision_view(request, subject_name):
    subject = get_object_or_404(Subject, name__iexact=subject_name.replace('-', ' ').title())
    materials = RevisionMaterial.objects.filter(subject=subject)
    return render(request, 'revision.html', {'subject': subject, 'materials': materials})

def mock_paper_view(request, subject_name):
    subject = get_object_or_404(Subject, name__iexact=subject_name.replace('-', ' ').title())
    papers = MockPaper.objects.filter(subject=subject)
    return render(request, 'mock_papers.html', {'subject': subject, 'papers': papers})

def pyq_view(request, subject_name):
    subject = get_object_or_404(Subject, name__iexact=subject_name.replace('-', ' ').title())
    papers = PYQPaper.objects.filter(subject=subject).order_by('-year')
    return render(request, 'pyq_papers.html', {'subject': subject, 'papers': papers})


# =====================================================
# 9. 🔐 CONTENT VIOLATION LOGGER
# =====================================================

@login_required
@require_POST
def log_content_violation(request):
    """
    Logs each content security violation.
    Visible live in Django Admin.
    """
    obj, _ = ContentViolation.objects.get_or_create(user=request.user)
    obj.count += 1
    obj.last_violation = timezone.now()
    obj.save()

    return JsonResponse({
        "status": "ok",
        "count": obj.count
    })