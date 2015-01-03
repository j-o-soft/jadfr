from django.db.models import manager, QuerySet, Model
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

    def _fetch_all(self):
        """
        get the item(s) and call the callback if necessary.
        """
        super(CallbackManagerQuerySet, self)._fetch_all()
        logger.debug('Callback: %s', self.callback)
        if self.callback:
            map(lambda item: self.callback(item, **self.call_kwargs), self._result_cache)


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

    def qet_queryset(self):
        return self._queryset_class(self.model,
                                    using=self._db,
                                    hints=self._hints,
                                    callback=self.callback,
                                    call_kwargs=self.call_kwargs)