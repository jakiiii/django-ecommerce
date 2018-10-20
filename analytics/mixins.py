# Custom mixins, specifically Class or generic view
from .signals import object_viewed_signals


class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs)
        instance = context.get('object')
        if instance:
            object_viewed_signals.send(instance.__class__, instance=instance, request=self.request)
        return context
