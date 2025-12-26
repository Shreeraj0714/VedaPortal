from django.contrib import admin
from .models import (
    Profile, Product, Subject, Unit, Topic,
    RevisionMaterial, Question, MockPaper, PYQPaper,
    ContentViolation
)

# =====================================================
# 1. PRODUCT ADMIN
# =====================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price')
    prepopulated_fields = {'slug': ('name',)}


# =====================================================
# 2. PROFILE ADMIN
# =====================================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'payment_status',
        'is_premium_member',
        'get_products_count'
    )

    list_filter = ('payment_status', 'is_premium_member')
    search_fields = ('user__username',)
    filter_horizontal = ('unlocked_products',)
    actions = ['approve_payment', 'reject_payment']

    def get_products_count(self, obj):
        return obj.unlocked_products.count()
    get_products_count.short_description = "Items Owned"

    def approve_payment(self, request, queryset):
        queryset.update(payment_status='approved')
        self.message_user(request, "Selected payments marked as APPROVED.")
    approve_payment.short_description = "✅ Mark as Approved"

    def reject_payment(self, request, queryset):
        queryset.update(payment_status='pending')
        self.message_user(request, "Selected profiles set back to PENDING.")
    reject_payment.short_description = "❌ Reset to Pending"


# =====================================================
# 3. CONTENT ADMIN
# =====================================================
class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject',)
    search_fields = ('title',)
    inlines = [TopicInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch_code')


# 🔴 REQUIRED FIX — REGISTER TOPIC EXPLICITLY
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    search_fields = ('title',)
    list_filter = ('unit',)


# =====================================================
# 4. EXAM BOOSTER ADMIN
# =====================================================
@admin.register(RevisionMaterial)
class RevisionMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'category', 'unit')
    list_filter = ('subject', 'category')
    search_fields = ('title', 'content')


# =====================================================
# 5. QUESTION BANK ADMIN
# =====================================================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'short_question', 'subject', 'unit',
        'difficulty', 'probability', 'is_verified'
    )
    list_filter = ('subject', 'difficulty', 'is_verified')
    search_fields = ('question_text',)
    list_editable = ('probability', 'is_verified')

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if obj.question_text else ""
    short_question.short_description = "Question"


# =====================================================
# 6. MOCK PAPER ADMIN
# =====================================================
@admin.register(MockPaper)
class MockPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    list_filter = ('subject',)
    search_fields = ('title',)


# =====================================================
# 7. PREVIOUS YEAR PAPERS ADMIN
# =====================================================
@admin.register(PYQPaper)
class PYQPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'subject', 'created_at')
    list_filter = ('subject', 'year')
    search_fields = ('title', 'year')


# =====================================================
# 8. CONTENT VIOLATION ADMIN
# =====================================================
@admin.register(ContentViolation)
class ContentViolationAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'last_violation')
    search_fields = ('user__username',)
    list_filter = ('last_violation',)
