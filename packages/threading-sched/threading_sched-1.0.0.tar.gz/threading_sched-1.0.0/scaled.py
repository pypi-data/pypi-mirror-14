from __future__ import absolute_import
from __future__ import print_function

__author__                      = "Perry Kundert"
__email__                       = "perry@hardconsulting.com"
__copyright__                   = "Copyright (c) 2011 Hard Consulting Corporation"
__license__                     = "GPLv3 (or later)"

import itertools
from .default import scheduler
class scaled_scheduler(scheduler):
    '''
    Extend our (thread-safe) implementation of the Python sched.scheduler, to order events by age
    (time past due), scaled by priority.  

    if event.time is not expired, then scaled priority will be -'ve.  If event.priority is zero,
    all expired events will be equal, so the first one will win.  Otherwise, an event with
    priority == 2 will "seem" twice as old as an event with priority == 1.

    The implementation of next_event using itertools is more or less equivalent to:

    def next_event(self, now=None):

        def scale(event, now):
            return (event.time - now) * event.priority

        def expired(event, now):
            return event.time >= now

        with self._lock:
            if now is None:
                now = self.timefunc()
            queue = iter(self._queue)
            best = next(queue)
            bestvalue = scale(best)

            for event in queue:
                if not expired(event, now)
                    break
                value = scale(event, now)
                if value > bestvalue:
                    best, bestvalue = event, value
        return best
    '''
    def next_event(self, now=None):
        with self._lock:
            if now is None:
                now = self.timefunc()
            try:
                return max(				# Return the maximal event
                    itertools.takewhile(
                        lambda e: e.time <= now,	#   taking only expired events
                        self._queue),			#   from this queue
                    key=lambda e: (e.priority		#   maximizing this calculation
                                   * (now - e.time)))
            except ValueError:
                # No expired events.  Just return the earliest
                return self._queue[0]
                                               
