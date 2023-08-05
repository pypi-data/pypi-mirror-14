from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def get_admin_change_url(model_instance):
    info = (model_instance._meta.app_label, model_instance._meta.model_name)
    admin_url = reverse('admin:%s_%s_change' % info, args=(model_instance.pk,))
    return admin_url