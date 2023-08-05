# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin

from admin_monitoring.admin import admin_monitoring_mixin_factory


class VNP(object):
    """ для отображения числа новых компаний в админке """
    def __init__(self, model, vnp, **kwargs):
        self.model = model
        self.vnp_old = vnp
        self.kwargs = kwargs

    def __unicode__(self):
        # fixes UnicodeDecodeError
        return "%s" % self.__repr__()

    def replace(self, *args, **kwargs):
        """ govnocode fix for 'VNP' object has no attribute 'replace' """
        return self.__unicode__().replace(*args, **kwargs)

    def __repr__(self):
        count = self.model.objects.filter(**self.kwargs).count()
        if count:
            return "%s (%s)" % (self.vnp_old, count)
        else:
            return self.vnp_old


def register(admin_site, model, model_admin=admin.ModelAdmin,
             new_object_kwargs=None, seen_object_kwargs=None, **options):
    """ пример использования:
        register(admin.site, Model, ModelAdmin, {"viewed": False})
        таким образом возле названия модели
        будет подписано число объектов с аттрибутом viewed=False """
    if not new_object_kwargs:
        new_object_kwargs = {}

    if not seen_object_kwargs:
        if len(new_object_kwargs.keys()) == 1:
            seen_object_kwargs = {
                new_object_kwargs.keys()[0]: not new_object_kwargs.values()[0]
            }
        elif len(new_object_kwargs.keys()) > 1:
            raise Exception("seen_object_kwargs must be specified"
                            " in complex cases")
    AdminMonitoringMixin = admin_monitoring_mixin_factory(new_object_kwargs,
                                                          seen_object_kwargs)
    class ModelAdmin(AdminMonitoringMixin, model_admin):
        pass

    if not hasattr(model._meta, "_verbose_name_plural"):
        model._meta._verbose_name_plural = model._meta.verbose_name_plural
    model._meta.verbose_name_plural = VNP(model,
                                          model._meta._verbose_name_plural,
                                          **new_object_kwargs)

    admin_site.register(model, ModelAdmin, **options)
