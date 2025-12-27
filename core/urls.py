from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include


# Import ALL functions from your views.py
from main.views import (
    landing, college_our, college_wip,
    home, register, login_user, logout_user,
    payment, premium_content, packages,
    semester_subjects, subject_units, subject_syllabus,
    subject_view, topic_view,
    question_bank_view, revision_view, mock_paper_view,
    pyq_view,
    log_content_violation
)

urlpatterns = [

    # -------------------------
    # Admin
    # -------------------------
    path('admin/', admin.site.urls),
    
    
    path('api/', include('api.urls')),


    # -------------------------
    # CKEditor Image Uploader
    # -------------------------
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # -------------------------
    # Landing & Auth
    # -------------------------
    path('', landing, name='landing'),
    path('college/our/', college_our, name='college_our'),
    path('college/wip/', college_wip, name='college_wip'),

    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # -------------------------
    # Payment & Packages
    # -------------------------
    path('packages/', packages, name='packages'),
    path('payment/', payment, name='payment'),
    path('premium/', premium_content, name='premium'),

    # -------------------------
    # Dynamic Content
    # -------------------------
    path('subject/<str:subject_name>/', subject_view, name='subject_detail'),
    path('topic/<int:topic_id>/', topic_view, name='topic_reader'),

    # -------------------------
    # Exam Content
    # -------------------------
    path('subject/<str:subject_name>/question-bank/', question_bank_view, name='question_bank'),
    path('subject/<str:subject_name>/revision/', revision_view, name='revision_view'),
    path('subject/<str:subject_name>/mock-papers/', mock_paper_view, name='mock_paper_view'),
    path('subject/<str:subject_name>/pyq/', pyq_view, name='pyq_view'),

    # -------------------------
    # Content Violation Logger
    # -------------------------
    path(
        'log-content-violation/',
        log_content_violation,
        name='log_content_violation'
    ),

    # -------------------------
    # Old Academic Routes
    # -------------------------
    path('fy/<str:semester>/', semester_subjects, name='fy_semester'),
    path('fy/<str:semester>/<str:branch>/<str:subject>/syllabus/', subject_syllabus, name='subject_syllabus'),
    path('fy/<str:semester>/<str:branch>/<str:subject>/', subject_units, name='subject_units'),
]

# -------------------------
# Static & Media (DEV ONLY)
# -------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.urls import path
from django.http import HttpResponse
from django.contrib.sites.models import Site

# --- TEMPORARY FIXER VIEW ---
def fix_site_domain(request):
    try:
        # Get the default site (ID=1)
        site = Site.objects.get(id=1)
        
        # UPDATE THIS TO YOUR EXACT RAILWAY DOMAIN
        site.domain = 'web-production-5294.up.railway.app' 
        site.name = 'VedaPortal'
        site.save()
        
        return HttpResponse(f"<h1>✅ SUCCESS!</h1> <p>Domain updated to: {site.domain}</p> <p>You can now <a href='/admin/'>Login to Admin</a></p>")
    except Exception as e:
        return HttpResponse(f"<h1>❌ Error</h1> <p>{e}</p>")

# Add this to your urlpatterns list
urlpatterns += [
    path('fix-db/', fix_site_domain),
]