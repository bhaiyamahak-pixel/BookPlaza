from django.shortcuts import redirect

class RegisterRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt = ['/register/', '/admin/', '/media/', '/static/']
        if not request.session.get('customer_id') and not any(request.path.startswith(p) for p in exempt):
            return redirect('register')
        return self.get_response(request)

