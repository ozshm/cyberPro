def isauth_context_processor(request):
    return {
        'isAuthenticated': request.COOKIES.get('isAuthenticated'),
    }
