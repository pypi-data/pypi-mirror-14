from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.template import Template, Context


def admin_monitoring_mixin_factory(new_object_kwargs, seen_object_kwargs):
    class AdminMonitoringMixin(admin.ModelAdmin):
        def change_view(self, request, object_id, form_url='',
                        extra_context=None):
            # now the object is seen. we're applying our seen kwargs
            modified_kwargs = {}
            for k, v in seen_object_kwargs.items():
                if hasattr(v, "__call__"):
                    v = v()
                modified_kwargs[k] = v
            self.model.objects.filter(pk=object_id).update(**modified_kwargs)

            return super(AdminMonitoringMixin, self).change_view(
                request, object_id, form_url=form_url,
                extra_context=extra_context)

        def get_css_name(self):
            return '{}_{}_info_css'.format(self.model._meta.app_label,
                                           self.model._meta.model_name)

        def get_urls(self):
            urls = super(AdminMonitoringMixin, self).get_urls()
            additional_urls = patterns('',
                url(r'^info.css$', self.admin_site.admin_view(self.get_css_view), 
                    name=self.get_css_name())
            )
            return additional_urls + urls

        def get_css_view(self, request):
            new_items = self.model.objects.filter(**new_object_kwargs)
            template = Template("""
                {% load admin_monitoring_tags %}
                {% if items %}{% for item in items %}a[href="{% get_admin_change_url item %}"]{% if not forloop.last %},{% endif %} {% endfor %}{
                    font-weight: bold;
                    text-decoration: underline;
                    color: red;
                }{% endif %}
            """)

            return HttpResponse(template.render(Context({
                'items': new_items
            })), content_type="text/css")

        def _media(self):
            return forms.Media(css={
                'screen': [reverse_lazy('admin:{}'.format(self.get_css_name()))]
            })
        media = property(_media)

    return AdminMonitoringMixin
