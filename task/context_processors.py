from django.template import Context

def current_url(request):
  return {'current_url': request.path}
