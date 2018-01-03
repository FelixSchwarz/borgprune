# -*- coding: UTF-8 -*-

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY


__all__ = ['find_closest_archive', 'list_archives_since']

def find_closest_archive(datetime, archives):
    best = None
    best_difference = None
    for archive in archives:
        current_difference = abs(archive.time - datetime)
        if (best is None) or (current_difference < best_difference):
            best = archive
            best_difference = current_difference
    return best

def list_archives_since(start, archives):
    for archive in archives:
        if start <= archive.time:
            yield archive

def list_recurring_dates(frequency, start, end):
    # dateutil's rrule implements RFC 2445 which means invalid dates are ignored without any fallback:
    # For example this might lead to skipping February entirely for monthly rules starting at January 30.
    # In our use case we should not skip any month and we can easily fall back to either the previous or the following
    # valid date.
    #
    # RFC 7529 should contain extensions to mitigate that behavior but it is currently (December 2017) not implemented
    # in dateutil: https://github.com/dateutil/dateutil/issues/315
    # The workaround here is to use a custom function to generate monthly recurrence.
    if frequency == MONTHLY:
        month_delta = relativedelta(months=1)
        yield from disclosure_dates(start, month_delta, dtend=end)
    else:
        yield from rrule(freq=frequency, dtstart=start, until=end)


# ---------------------------------------------------------------------------------------------------------------------
# https://stackoverflow.com/a/38555283/138526
def disclosure_dates(dtstart, rd, dtend=None):
    ii = 0
    while True:
        # "ii*rd" helps so we are not permanently locked to the shortest month
        # (e.g. 2017-01-31 -> 2017-02-28 -> 2017-03-31 vs 2017-03-28)
        cdate = dtstart + ii*rd
        ii += 1

        yield cdate
        if dtend is not None and cdate >= dtend:
            break
# ---------------------------------------------------------------------------------------------------------------------
