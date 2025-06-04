from django import template
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

register = template.Library()

@register.simple_tag(takes_context=True)
def canonical_url(context, url=None):
    """
    Generate a canonical URL for the current page.
    Usage: {% canonical_url %}
    Or with specific URL: {% canonical_url url='https://example.com/page' %}
    """
    request = context.get('request')
    if not request:
        return ''

    if url:
        # If a specific URL is provided, validate it
        if url_has_allowed_host_and_scheme(url, allowed_hosts=settings.ALLOWED_HOSTS):
            return url
        return ''

    # Get the current URL without query parameters
    current_url = request.build_absolute_uri(request.path)
    
    # Remove trailing slash if it exists and the URL is not the root
    if current_url.endswith('/') and len(current_url) > 1:
        current_url = current_url[:-1]
    
    return current_url 