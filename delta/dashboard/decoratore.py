from django.shortcuts import render



def role_required(allowed_roles = []):
    def decorator(func):
        def wrap(request,*args,**kwargs):
            if request.user.role in allowed_roles:
                return func(request,*args,**kwargs)
            else:
                return render(request,"html/dashboard/access_denied.html")
        return wrap
    return decorator
def role_blocked(blocked_roles = []):
    def decorator(func):
        def wrap(request,*args,**kwargs):
            if request.user.role not in blocked_roles:
                return func(request,*args,**kwargs)
            else:
                return render(request,"html/dashboard/access_denied.html")
        return wrap
    return decorator
