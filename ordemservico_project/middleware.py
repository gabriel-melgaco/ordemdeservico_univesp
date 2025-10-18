from datetime import datetime, timedelta
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        last_touch = request.session.get('last_touch', datetime.now())
        if datetime.now() - last_touch > timedelta(minutes=10):  # Tempo limite
            logout(request)
        request.session['last_touch'] = datetime.now()
