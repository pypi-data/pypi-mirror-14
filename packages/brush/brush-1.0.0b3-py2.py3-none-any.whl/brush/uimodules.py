"""Web UI modules."""

import logging
from tornado.web import UIModule
from .stores import store

logger = logging.getLogger('web')


class CurrentValue(UIModule):
    def render(self, key, name=None, lockbox_key=None):
        """Displays the current value of a data key.

        Parameters
        ----------
        key : str
            Data key to show the value of
        name : str or None
            Display name or the ``key`` if None
        lockbox_key : str or None
            Data key for associated lockbox if any

        """
        data = store.get()
        if key not in data:
            logger.error('invalid key: ' + key)
            return

        name = name or key

        if lockbox_key is not None and lockbox_key not in data:
            locked = None
            logger.warn('Invalid lockbox key requested: ' + lockbox_key)
        else:
            locked = data[lockbox_key]

        return self.render_string('current-value.html', key=key,
                                  value=data[key], name=name, locked=locked)
