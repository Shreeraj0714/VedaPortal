from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# For Single Session, Real-time Logic & Signals
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save # Added for auto-profile creation
from django.dispatch import receiver
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# =====================================================
# 1. MAIN CONTENT MODELS (Subject -> Unit -> Topic)
# =====================================================

class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50, default="FY_COMMON") 
    
    def __str__(self):
        return self.name


class Unit(models.Model):
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subject.name} - {self.title}"


class Topic(models.Model):
    unit = models.ForeignKey(Unit, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField(help_text="Write your notes here")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# =====================================================
# 2. EXAM BOOSTER / REVISION
# =====================================================

class RevisionMaterial(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextField(help_text="Enter the full study material/summary here")

    CATEGORY_CHOICES = [
        ('cheat_sheet', 'Formula Cheat Sheet'),
        ('summary', 'One-Page Summary'),
        ('study_plan', '2-Hour Study Plan'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='summary')

    def __str__(self):
        return f"{self.subject.name} - {self.title}"


# =====================================================
# 3. QUESTION BANK
# =====================================================

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    question_text = RichTextField()
    answer_text = RichTextField(help_text="Model Answer")

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    probability = models.IntegerField(default=90)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.subject.name}] {self.question_text[:50]}..."


# =====================================================
# 4. MOCK PAPERS
# =====================================================

class MockPaper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    paper_content = RichTextField()
    solution_content = RichTextField()

    def __str__(self):
        return f"{self.subject.name} - {self.title}"


# =====================================================
# 5. PREVIOUS YEAR PAPERS (PYQ)
# =====================================================

class PYQPaper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='pyq_papers')
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    paper_content = RichTextField()
    solution_content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.subject.name}"


# =====================================================
# 6. PRODUCT MODEL
# =====================================================

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    price = models.IntegerField(default=49)

    def __str__(self):
        return f"{self.name} (₹{self.price})"


# =====================================================
# 7. PROFILE MODEL
# =====================================================

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Required for registration fix
    payment_name = models.CharField(max_length=100, blank=True, null=True)
    payment_ref = models.CharField(max_length=100, blank=True, null=True)

    payment_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('approved', 'Approved')], 
        default='pending'
    )
    unlocked_products = models.ManyToManyField(Product, blank=True)
    is_premium_member = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# =====================================================
# 8. CONTENT VIOLATION TRACKING
# =====================================================

class ContentViolation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    last_violation = models.DateTimeField(auto_now=True)


# =====================================================
# 9. INSTANT SINGLE SESSION ENFORCEMENT
# =====================================================

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    1. Middleware Support: Saves the new session key to cache.
    2. Instant Logout: Broadcasts a kill signal to WebSockets.
    """
    session_key = request.session.session_key
    cache.set(f'user_session_{user.id}', session_key, 86400)

    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "force_logout",
                "message": "Security Alert: You have been logged out because a new login was detected on another device."
            }
        )

# =====================================================
# 10. AUTO-CREATE PROFILE SIGNALS
# =====================================================

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile object whenever a new User is created.
    """
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        # If user is updated, ensure profile exists and save it
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)