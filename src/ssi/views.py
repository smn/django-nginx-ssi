from django.http import HttpResponse
from django.template import Template, RequestContext
from django.core.cache import cache

def render_from_cache(request, cache_key):
    template = Template(cache.get(cache_key, ''))
    context = cache.get('%s:context' % cache_key, {})
    request_context = RequestContext(request, context)
    return HttpResponse(template.render(request_context))
    