from hashlib import md5
import logging

from django.utils import six
from django.dispatch import receiver
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.core.cache.backends.dummy import DummyCache
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str
from cache_tools import conf

log = logging.getLogger('cache_tools.utils')


@receiver(post_save)
@receiver(post_delete)
def invalidate_cache(sender, instance, **kwargs):
    try:
        invalidate_cache_for_object(instance)
    except RuntimeError:
        # in Django 1.7 and higher can be raised RuntimeError if sender is Migration model
        log.debug('Can not invalidate cache for %s with pk %s' % (sender, getattr(instance, 'pk', None)), exc_info=True)


def invalidate_cache_for_object(obj):
    key = _get_key(conf.KEY_PREFIX, ContentType.objects.get_for_model(obj), pk=obj.pk, version_key=True)
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=conf.CACHE_TIMEOUT)


def normalize_key(key):
    if len(key) < 65:
        return key
    if six.PY3:
        key = key.encode("utf-8", "replace")
    return md5(key).hexdigest()


def _get_key(start, model, pk=None, version_key=False, **kwargs):

    if pk and not kwargs:
        key = ':'.join((
            start, str(model.pk), str(pk)
        ))
        if version_key:
            return key + ':VER'
        version = cache.get(key + ':VER') or '0'
        return '%s:%s' % (key, version)

    for key, val in six.iteritems(kwargs):
        if hasattr(val, 'pk'):
            kwargs[key] = val.pk

    return normalize_key(':'.join((
        start,
        str(model.pk),
        ','.join(':'.join((key, smart_str(kwargs[key]))) for key in sorted(kwargs.keys()))
    )))


def get_cached_object(model, timeout=conf.CACHE_TIMEOUT, **kwargs):
    """
    Return a cached object. If the object does not exist in the cache, create it.

    Params:
        model - ContentType instance representing the model's class or the model class itself
        timeout - TTL for the item in cache, defaults to CACHE_TIMEOUT
        **kwargs - lookup parameters for content_type.get_object_for_this_type and for key creation

    Throws:
        model.DoesNotExist is propagated from content_type.get_object_for_this_type
    """
    if not isinstance(model, ContentType):
        model_ct = ContentType.objects.get_for_model(model)
    else:
        model_ct = model

    key = _get_key(conf.KEY_PREFIX, model_ct, **kwargs)

    obj = cache.get(key)
    if obj is None:
        # fetch the actual object we want
        obj = model_ct.model_class()._default_manager.get(**kwargs)

        # since 99% of lookups are done via PK make sure we set the cache for
        # that lookup even if we retrieved it using a different one.
        if 'pk' in kwargs:
            cache.set(key, obj, timeout)
        elif not isinstance(cache, DummyCache):
            cache.set_many({key: obj, _get_key(conf.KEY_PREFIX, model_ct, pk=obj.pk): obj}, timeout=timeout)

    return obj

RAISE, SKIP, NONE = 0, 1, 2


def get_cached_objects(pks, model=None, timeout=conf.CACHE_TIMEOUT, missing=RAISE):
    """
    Return a list of objects with given PKs using cache.

    Params:
        pks - list of Primary Key values to look up or list of content_type_id, pk tuples
        model - ContentType instance representing the model's class or the model class itself
        timeout - TTL for the items in cache, defaults to CACHE_TIMEOUT

    Throws:
        model.DoesNotExist is propagated from content_type.get_object_for_this_type
    """
    if model is not None:
        if not isinstance(model, ContentType):
            model = ContentType.objects.get_for_model(model)
        pks = [(model, pk) for pk in pks]
    else:
        pks = [(ContentType.objects.get_for_id(ct_id), pk) for (ct_id, pk) in pks]

    keys = [_get_key(conf.KEY_PREFIX, model, pk=pk) for (model, pk) in pks]

    cached = cache.get_many(keys)

    # keys not in cache
    keys_to_set = set(keys) - set(cached.keys())
    if keys_to_set:
        # build lookup to get model and pks from the key
        lookup = dict(zip(keys, pks))

        to_get = {}
        # group lookups by CT so we can do in_bulk
        for k in keys_to_set:
            ct, pk = lookup[k]
            to_get.setdefault(ct, {})[int(pk)] = k

        to_set = {}
        # retrieve all the models from DB
        for ct, vals in to_get.items():
            models = ct.model_class()._default_manager.in_bulk(vals.keys())
            for pk, m in models.items():
                k = vals[pk]
                cached[k] = to_set[k] = m

        if not isinstance(cache, DummyCache):
            # write them into cache
            cache.set_many(to_set, timeout=timeout)

    out = []
    for k in keys:
        try:
            out.append(cached[k])
        except KeyError:
            if missing == NONE:
                out.append(None)
            elif missing == SKIP:
                pass
            elif missing == RAISE:
                ct = ContentType.objects.get_for_id(int(k.split(':')[1]))
                raise ct.model_class().DoesNotExist(
                    '%s matching query does not exist.' % ct.model_class()._meta.object_name)
    return out


def get_cached_object_or_404(model, timeout=conf.CACHE_TIMEOUT, **kwargs):
    """
    Shortcut that will raise Http404 if there is no object matching the query

    see get_cached_object for params description
    """
    try:
        return get_cached_object(model, timeout=timeout, **kwargs)
    except ObjectDoesNotExist as e:
        raise Http404('Reason: %s' % str(e))


def cache_this(key_getter, timeout=conf.CACHE_TIMEOUT):
    def wrapped_decorator(func):
        def wrapped_func(*args, **kwargs):
            key = key_getter(*args, **kwargs)
            if key is not None:
                result = cache.get(key)
            else:
                result = None
            if result is None:
                log.debug('cache_this(key=%s), object not cached.', key)
                result = func(*args, **kwargs)
                cache.set(key, result, timeout)
            return result

        wrapped_func.__dict__ = func.__dict__
        wrapped_func.__doc__ = func.__doc__
        wrapped_func.__name__ = func.__name__

        return wrapped_func
    return wrapped_decorator
