from django import template
from django.urls import resolve

from master_data.models import JadwalTenagaMedis

register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumb(context):
    request = context['request']
    current_path = request.path
    breadcrumbs = []

    try:
        for part in current_path.split('/'):
            if part:
                url = f'/{"/".join(breadcrumbs + [part])}/'
                view = resolve(url)
                breadcrumbs.append({
                    'title': view.url_name.replace('_', ' ').replace('-', ' ').title(),
                    'url': url
                })
        return breadcrumbs
    except Exception:
        return []

@register.filter(takes_context=True)
def get_days(tenaga_medis):
    return JadwalTenagaMedis.objects.filter(tenaga_medis=tenaga_medis)