"""
=============================================================
 Admin Profile Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Admin can view profile.
    - Session-based login enforced.
=============================================================
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import Login
from login.views import session_required

@session_required('Admin_login')
def admin_profile(request):
    """
    View admin profile.
    Session login required for Admin.
    """
    username = request.session.get('login_username')
    try:
        admin_obj = Login.objects.get(username=username, role='Admin')
    except Login.DoesNotExist:
        messages.error(request, "Admin data not found.")
        return redirect('admin')

    return render(request, 'login/admin_profile.html', {'admin': admin_obj})
