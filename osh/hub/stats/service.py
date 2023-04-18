import datetime
import logging
import types

from osh.hub.stats import stattypes
from osh.hub.stats.models import StatResults, StatType

logger = logging.getLogger(__name__)


def get_last_stat_result(stat_type, release=None):
    if release:
        result = StatResults.objects.filter(stat=stat_type, release=release)
    else:
        result = StatResults.objects.filter(stat=stat_type)
    if result:
        return result.latest()


def get_mapping():
    """
    Return mapping between statistical function and its properties:
        { function: (tag, short_comment, comment, group, order), }
    """
    mapping = {}
    for binding_name in dir(stattypes):
        binding = getattr(stattypes, binding_name)
        if isinstance(binding, types.FunctionType) and\
                binding.__name__.startswith('get_'):
            mapping[binding] = (binding.__name__[4:].upper(),
                                binding.short_comment, binding.comment,
                                binding.group, binding.order,
                                )
    return mapping


def create_stat_result(key, value, release=None):
    """
    Helper function that stores statistical result. If the result is same as
     in previous run, do not store it
    """
    stat_type = StatType.objects.get(key=key)
    last_stat = get_last_stat_result(stat_type, release)
    if not value:
        value = 0
    if not last_stat or last_stat.value != value:
        s = StatResults()
        s.stat = stat_type
        s.value = value
        if release is not None:
            s.release = release
        s.save()


def update():
    """
    Refresh statistics data.
    """
    logger.info('Update statistics.')
    for func, desc in get_mapping().items():
        stat_data = func()
        if isinstance(stat_data, int):
            create_stat_result(desc[0], stat_data)
        elif isinstance(stat_data, dict):
            for s in stat_data:
                create_stat_result(desc[0], stat_data[s], s)


def display_values(stat_type, release=None):
    if release:
        results = StatResults.objects.filter(stat=stat_type, release=release)
    else:
        results = StatResults.objects.filter(stat=stat_type)

    if not results:
        return {datetime.datetime.now(): 0}

    return {res.date: res.value for res in results.order_by('-date')}
