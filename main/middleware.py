class SessionDefaultMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, есть ли уже есть значение, чтобы не перезаписывать его
        if 'my_key' not in request.session:
            request.session['my_key'] = 'default_value'
        
        response = self.get_response(request)
        return response