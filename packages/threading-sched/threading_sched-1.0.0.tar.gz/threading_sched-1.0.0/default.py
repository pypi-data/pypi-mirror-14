from __future__ import absolute_import
from __future__ import print_function

__author__                      = "Perry Kundert"
__email__                       = "perry@hardconsulting.com"
__copyright__                   = "Copyright (c) 2011 Hard Consulting Corporation"
__license__                     = "GPLv3 (or later)"

import threading
import sched

class scheduler(sched.scheduler):
    """
    Thread-safe implementation of the stock Python sched.scheduler class.  The API remains basically
    the same, with some optional additions to support creating custom prioritization schemes.

    We implement locking for thread safety, and we awaken our run method whenever the events in the
    list might have changed in a way that could shorten our timeout.
    
    The following are extensions to the Python sched.scheduler API:

    - Keyword Arguments
        In enter{abs}(), an optional kwargs argument may be provided, containing a dictionary of 
        keyword arguments to pass to the function.  

        def enterabs(self, time, priority, action, argument, kwargs={}):
    
    """
    def __init__(self, *args, **kwargs):
        sched.scheduler.__init__(self, *args, **kwargs)
        if not hasattr( self, '_lock' ):
            self._lock = threading.RLock() # < Python 3.3
        self._cond = threading.Condition( self._lock )

    def enterabs(self, time, priority, action, argument, kwargs=None):
        """Assumes enter() uses enterabs().  Since our Condition uses our RLock, we can safely acquire the
        Condition, and issue the notify_all; it won't be delivered 'til we fully release our
        self._lock.  Since base sched.scheduler is an old-style class in Python 2, don't use super.

        """
        if kwargs is None:
            kwargs = {}
        with self._cond:
            if hasattr( sched.Event, 'kwargs' ): # iff >= Python3
                e = sched.scheduler.enterabs( self, time, priority, action, argument, kwargs )
            else:
                # Prepare a closure to wrap the action, trapping the supplied keyword kwargs (if
                # any).  If *any* keyword arguments are supplied, then they will be passed to the
                # action along with the event arguments.
                e = sched.scheduler.enterabs(
                    self, time, priority, lambda *args: action( *args, **kwargs ), argument )
            # Awaken any thread awaiting on a condition change, eg .run(), or .wait()
            self._cond.notify_all()
        #print "Scheduling %s" % ( str(e) )
        return e

    def enter(self, delay, priority, action, argument, kwargs=None):
        return self.enterabs(self.timefunc() + delay, priority, action, argument, kwargs=kwargs)

    def cancel(self, *args, **kwargs):
        """Removing an event can only result in us awakening too early, which is generally not a problem.
        However, if this empties the queue completely, we want run() to wake up and return right
        away!

        """
        with self._cond:
            e = sched.scheduler.cancel(self, *args, **kwargs)
            self._cond.notify_all()
        return e

    def empty(self):
        with self._lock:
            return sched.scheduler.empty(self)

    def wait(self):
        """
        Awaits a change in condition that could mean that there are now events to process.  Use this
        when the queue is (or might be) empty, and a thread needs to wait for something to process.
        """
        with self._cond:
            if self.empty():
                self._cond.wait()

    def next_event(self, now=None):
        """
        Return the next scheduled event, without removing it from the queue.  Throws an exception if
        none available.  Override this method to implement other priority schemes.
        """
        with self._lock:
            return self._queue[0]			# Strictly by time, then priority

    def run(self, pred=None):
        """
        Retrieve an event, waiting and looping if it hasn't expired.  Otherwise, remove it from the
        schedule, and run it.  Unlike the underlying sched.scheduler, this implementation waits in a
        multithreading sensitive fashion; if a new event is scheduled, we'll awaken and re-schedule
        our next wake-up.

        Returns when there are no more events left to run, or until the supplied predicate evaluates
        False.

        
        This run method is not usually appropriate to use directly as a Thread.run method, because
        it returns when the schedule is empty; this often doesn't mean the program is done.  To
        safely process events, a Thread must know (somehow) that the overall program is not yet
        complete, and implement its own run method like this, waiting for more events to be
        scheduled each time scheduler.run returns:

        class scheduler_thread(Thread):
            def __init__(self):
                self.sch = sched.scheduler(...)
                ...
            def run(self):
                while ( ... we are not finished ... ):
                    self.sch.run()
                    self.sch.wait()

        """
        while True if pred is None else pred():
            # Get the next event, relative to the current time. When schedule is empty, we're done.
            now = self.timefunc()
            with self._cond:				# Acquires self._lock
                if self.empty():
                    break

                # Queue is not empty, guaranteed
                event = self.next_event(now=now)
                if now < event.time:
                    # Next event hasn't expired; Wait 'til expiry, or an self._cond.notify...()
                    self._cond.wait(event.time - now)	# Releases self._lock
                    #print "Schedule condition wait expired after %fs" % (self.timefunc() - now)
                    continue
                    # TODO: this is inefficient pre-3.2, due to a busy wait loop in the
                    # threading Condition.  Perhaps we should detect this, and implement in
                    # terms of spawning another Thread to sleep 'til the desired time, then
                    # trigger .notify_all()?

                # An expired event is detected.  No schedule modification can have occurred (we hold
                # the lock, and no self._cond.wait() has been processed, because it always will
                # 'continue' the loop) so we can safely cancel it.  We can make no assumptions about
                # its position in the _queue, to allow arbitrary scheduling algorithms.
                self.cancel(event)

            # Trigger the expired (and removed) event's action wrapper function.  This may result in
            # schedule modification, so we do this outside the lock.  If func raises an exception,
            # the scheduler's invariant is maintained, and this method may be called again.
            #print "Scheduled event firing: %s" % (str(event))
            if hasattr( event, 'kwargs' ): # iff >= Python3
                event.action( *event.argument, **event.kwargs )
            else:
                event.action( *event.argument )
            self.delayfunc(0)				# Let other threads run

