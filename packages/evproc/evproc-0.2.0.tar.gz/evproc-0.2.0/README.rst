=========================
Event Processor Framework
=========================

EvProc is a framework for building complex event processors.  There
are many similar frameworks available, so why EvProc?  EvProc provides
a few advantages.  First, a ``@want()`` decorator is available to
pre-filter events, as opposed to registering an event handler on
specific events.  (Filtering works primarily with an event name,
allowing flexibility, but it is also possible to register arbitrary
filter functions, which can evaluate an event to determine whether to
call the event handler.)  A second advantage is the ability to
register event handlers using the "entrypoint" support of
``setuptools``, allowing extensibility.  Finally, EvProc provides
limited inter-handler communication, using the ``proc`` property of
``Event`` instances, and backs this up with the ability to specify
ordering among event handlers using requirements.

Defining Events
===============

An *event* in EvProc is an instance of a subclass of ``evproc.Event``.
The ``Event`` class is an abstract class; subclasses must implement a
``name`` property, the contents of which will be a unique string
naming the event.  The constructor takes a single optional argument, a
``ctxt`` argument, which may be used to pass a context in to event
handlers.  The constructor may, of course, be extended as required to
provide any necessary information about the event, such as a specific
resource that the event occurred on.

The ``Event`` class also provides a special ``proc`` property.  This
property may be used by event handlers to store data for use by other
event handlers, by setting attributes.  To minimize the possibility of
two unrelated handlers attempting to manipulate the same attribute,
the ``proc`` property is *namespaced*; that is, attributes on ``proc``
may not be set, but attributes on those attributes may.

As an example of the use of the ``proc`` property, consider two event
handlers that wish to communicate with each other.  Assume that these
handlers interact to perform testing; perhaps one handler selects test
parameters, and the second handler actually performs the test (e.g.,
there may be multiple tests to perform).  The first handler could set,
say, ``proc.tests.args`` and ``proc.tests.kwargs``, and the second
handler would then retrieve the values it needed.

Event Handlers
==============

An *event handler* is simply a function that will be called with two
arguments; the first argument will be an instance of
``evproc.Processor`` (described below), and the second will be an
instance of ``evproc.Event`` (described above).  The event handler may
perform any code necessary to process the event.  Each event handler
must have a unique name; by default, the name will be the same as the
function name, but this may be overridden when registering the event
handler.  Event handlers may also be loaded from ``setuptools``
entrypoints; in this case, the name used is the entrypoint name.

There are three optional decorators that may be used on an event
handler function.  The first is the ``@evproc.want()`` decorator,
which may be called with one or more event names; the handler function
will only be called if the event being handled matches one of these
event names.  The decorator may also be passed one or more *filter
functions*; in this case, the event handler will only be called if all
of the filter functions return ``True``.  If event names are also
passed, then the event must also match one of those names.  The
``@want()`` decorator may be used multiple times to specify other sets
of filters; the event need only match *one* filter specified by
``@want()``.  For instance, consider this example::

    @evproc.want('ev1', 'ev2')
    @evproc.want('ev3', lambda ev: ev.resource.name == 'resource')
    def handler(proc, ev):
        ...

This handler will be called for all events with the names "ev1" and
"ev2", but will only be called for the event "ev3" if
``ev.resource.name`` contains the value ``"resource"``.

Event handlers are able to interact with each other, as mentioned
above.  To do this, it is necessary to enforce certain ordering
guarantees on the event handler.  This is controlled by the
``@evproc.requires()`` and ``@evproc.required_by()`` decorators.
These decorators take the names of one or more event handlers (names
are set at registration time, as mentioned above).  The
``@requires()`` decorator is used to indicate that the specified
functions must run *before* the decorated function, while the
``@required_by()`` decorator is used to indicate that the specified
function require the *decorated* function to be run first.  In both
cases, the ``@want()`` decorators of the functions must be compatible.

The ``@requires()`` and ``@required_by()`` decorators are used to
define a *dependency graph*, which is then topologically sorted to
ensure that the handler functions are called in the correct order.  As
an example, consider the split test functions mentioned above.  We
could declare the functions like so::

    def test_prepare(proc, ev):
        ...
        ev.tests.args = args
        ev.tests.kwargs = kwargs

    @evproc.requires('test_prepare')
    def test_run(proc, ev):
        args = ev.tests.args
        kwargs = ev.tests.kwargs
        intermediate = getattr(ev.tests, 'auxiliary', [])
        ...

    @evproc.required_by('test_run')
    @evproc.requires('test_prepare')
    def test_auxiliary(proc, ev):
        ...
        ev.tests.auxiliary = results

In this example, the ``test_prepare()`` handler function would be
called first, followed by the ``test_auxiliary()`` handler function,
and finally the ``test_run()`` handler function would be called.

An event handler may optionally return a list of events, which will
be processed in order.

The Event Processor
===================

The ``evproc.Processor`` class is responsible for processing events.
To use EvProc, instantiate a ``Processor`` instance and use its
``register()`` or ``load_from()`` methods to declare event handler
functions.  Then, simply pass ``Event`` instances to the ``process()``
method to invoke the event processors in the correct order.

The ``Processor.register()`` method may be used to register individual
event handler functions.  By default, the function's declared name
(``func.__name__``) is used as the handler name, but this may be
overridden by passing the optional ``name`` parameter to
``register()``.

To load event handlers from a ``setuptools`` entrypoint, use the
``Processor.load_from()`` method.  This method takes, as its sole
argument, the entrypoint group name; as an example, if one installed
application has a ``setup.py`` containing::

    entry_points={
        'app.handlers': [
            'test_prepare = app:test_prepare',
            'test_run = app.test_run',
        ],
    }

And if a second installed application has the following in its
``setup.py``::

    entry_points={
        'app.handlers': [
            'test_auxiliary = otherapp:test_auxiliary',
        ],
    }

Then all three handler functions could be loaded into the
``Processor`` instance ``proc`` with the following call::

    proc.load_from('app.handlers')

The ``Processor.process()`` method may be called as many times as
necessary.  In fact, most event-driven applications consist of a loop
which constructs ``Event`` instances, then passes them to the
``Processor.process()`` method.  A full application could look
something like the following::

    def main():
        proc = evproc.Processor()
        proc.load_from('app.handlers')

        while True:
            # Construct event objects
            ...
            ev = AppEvent(...)

            # Process the event
            proc.process(ev)

``Processor.process()`` returns ``None`` unless an event processor
raises a ``evproc.StopProcessing`` exception initialized with a
``retval``, in which case it returns the exception's ``retval``.

Stop Processing
---------------

It may be necessary for one event processor to stop all event
processing.  This could, for instance, be used by a processor that
performs an authorization check if the event fails that check.  To
allow this, an event processor may raise the ``evproc.StopProcessing``
exception.  When an event processor raises a ``StopProcessing``
exception, no additional event processors will be called for that
event.  If the ``StopProcessing`` exception is raised without a
``retval``, yet-unprocessed events returned by prior event processors
will still be processed.  If the ``StopProcessing`` exception is
raised with a ``retval`` (even if ``None``), ``Processor.process()``
will immediately return the exception's ``retval``, and yet-unprocessed
events returned by prior event processors will not be processed.

Conclusion
==========

EvProc provides an easy to extend event processing framework, capable
of not only calling event handler functions, but of ensuring certain
ordering constraints and limited inter-handler communication.  The
ability to use ``setuptools`` entrypoints allows new event handlers to
be inserted into the event processing loop easily without having to
modify the original application, and the ordering constraints can
allow such inserted event handlers to interact with the existing ones
just as easily.
