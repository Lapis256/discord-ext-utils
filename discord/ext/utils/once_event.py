class OnceEvent:
    def dispatch(self, event_name, *args, **kwargs):
        super().dispatch(event_name, *args, **kwargs)
        ev = 'once_' + event_name
        try:
            coro = getattr(self, ev)
        except AttributeError:
            pass
        else:
            if coro is not None:
                self._schedule_event(coro, ev, *args, **kwargs)
                setattr(self, ev, None)

        for event in self.extra_events.pop(ev, []):
            self._schedule_event(event, ev, *args, **kwargs)
