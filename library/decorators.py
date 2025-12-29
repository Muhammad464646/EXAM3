from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user_role = request.user.userrole.role
            if user_role == 'admin':
                return view_func(request, *args, **kwargs)

            if user_role not in allowed_roles:
                return redirect('no_access')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
