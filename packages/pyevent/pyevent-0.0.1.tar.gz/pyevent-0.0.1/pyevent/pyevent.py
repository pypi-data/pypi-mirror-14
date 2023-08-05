__author__ = 'andy'


class Pyevent(object):
    """
    An eventing system based on the javascript microevent framework. It
    follows a publish subscribe pattern to call certain methods that are
    linked to events when those events are triggered.
    """

    def __init__ (self):
        # <String, Array<Function>> dictionary
        self._events = {}

    def bind (self, event, callback):
        """
        Bind an event to a call function and ensure that it is called for the
        specified event
        :param event: the event that should trigger the callback
        :type event: str
        :param callback: the function that should be called
        :rtype callback: function
        """
        if self._events.has_key(event):
            self._events[event].append(callback)
        else:
            self._events[event] = [callback]

    def unbind (self, event, callback):
        """
        Unbind the callback from the event and ensure that it is never called
        :param event: the event that should be unbound
        :type event: str
        :param callback: the function that should be unbound
        :rtype callback: function
        """
        if self._events.has_key(event) and len(self._events[event]) > 0:
            for _callback in self._events[event]:
                if _callback == callback:
                    self._events[event].remove(callback)
                if len(self._events[event]) == 0:
                    del self._events[event]

    def trigger (self, event, *args, **kwargs):
        """
        Cause the callbacks associated with the event to be called
        :param event: the event that occurred
        :type event: str
        :param data: optional data to pass to the callback
        :type data: anything that should be passed to the callback
        """
        if self._events.has_key(event):
            for _callback in self._events[event]:
                try:
                    _callback(args, kwargs)
                except TypeError:
                    _callback()


def mixin (cls):
    """
    A decorator which adds event methods to a class giving it the ability to
    bind to and trigger events

    :param cls: the class to add the event logic to
    :type cls: class
    :return: the modified class
    :rtype: class
    """
    cls._events = {}
    cls.bind = Pyevent.bind.__func__
    cls.unbind = Pyevent.unbind.__func__
    cls.trigger = Pyevent.trigger.__func__
    return cls
