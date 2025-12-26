from django.shortcuts import redirect
from django.contrib import messages

def premium_required(view_func):
    def wrapper(request, *args, **kwargs):
        # 1. Check Login
        if not request.user.is_authenticated:
            return redirect('login')

        profile = request.user.profile

        # 2. Check Pending Status
        if profile.payment_status == 'pending':
            messages.warning(
                request,
                "Your payment is under review. Access will be granted shortly."
            )
            return redirect('payment')

        # 3. Check Access (New Logic)
        # We check if they are a "Premium Member" (VIP) OR if they own at least 1 product
        has_any_product = profile.unlocked_products.exists()
        is_vip = profile.is_premium_member

        if not (is_vip or has_any_product):
            messages.error(
                request,
                "You need to unlock a package to view this content."
            )
            return redirect('packages')

        return view_func(request, *args, **kwargs)

    return wrapper