from django.db.models import manager, QuerySet
from logging import getLogger

logger = getLogger(__name__)


class CallbackManagerQuerySet(QuerySet):
    """
    calls the callback for every item in the queryset when it is accessed

    usage:
    qs(func).all() or qs.filter(...)(func)
    this will call func(item) for all items
    """

    def __init__(self, model=None, query=None, using=None, hints=None, callback=None, call_kwargs={}):
        super(CallbackManagerQuerySet, self).__init__(
            model=model,
            query=query,
            using=using,
            hints=hints)
        self.callback = callback
        self.call_kwargs = call_kwargs

    def __call__(self, callback, call_kwargs={}):
        """
        Sets the callback and call_kwargs for this queryset
        """
        clone = self._clone()
        clone.callback = callback
        clone.call_kwargs = call_kwargs.copy()
        return clone

    def _clone(self, klass=None, setup=False, **kwargs):
        """
        contributes the callback to the cloned qs
        """
        # because there happens a lot of stuff in _clone we don't overwrite it but we
        # set it after it's cloned
        val = super(CallbackManagerQuerySet, self)._clone(klass=klass, setup=setup, **kwargs)
        if not klass or issubclass(klass, CallbackManagerQuerySet):
            val.callback = self.callback
            val.call_kwargs = self.call_kwargs
        return val

    def get(self, *args, **kwargs):
        item = super(CallbackManagerQuerySet, self).get(*args, **kwargs)
        if self.callback:
            logger.debug('Callback: %s', self.callback)
            self.callback(item, **self.call_kwargs)
        return item

    def iterator(self):
        base_iterator = super(CallbackManagerQuerySet, self).iterator()
        items = (item for item in base_iterator)
        for item in items:
            if self.callback:
                logger.debug('Callback: %s', self.callback)
                self.callback(item, **self.call_kwargs)
            yield item


class CallbackManager(manager.Manager):
    """
    calls the callback for every item in the queryset when it is accessed

    usage:
    model.objects(func).all()
    this will call func(item) for all items
    """

    _queryset_class = CallbackManagerQuerySet

    def __call__(self, callback, **kwargs):
        """
        set the callback which should be used
        :param callback:
        :param kwargs:
        :return:
        """
        self.callback = callback
        self.call_kwargs = kwargs.copy()
        return self

    def get_queryset(self):
        callback = getattr(self, 'callback', None)
        call_kwargs = getattr(self, 'call_kwargs', None)
        return self._queryset_class(self.model,
                                    using=self._db,
                                    hints=self._hints,
                                    callback=callback,
                                    call_kwargs=call_kwargs)
