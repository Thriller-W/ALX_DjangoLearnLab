# LibraryProject/middleware.py
"""
Simple middleware to add Content-Security-Policy header.
Adjust the policy string to allow any CDN or third-party domains you need.
"""
class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # conservative default policy - allow only same-origin resources
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' data:; "
            "connect-src 'self';"
        )
        response['Content-Security-Policy'] = csp_policy
        return response
