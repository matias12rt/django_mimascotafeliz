from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return redirect('index')  
        return view_func(request, *args, **kwargs)
    return wrapper