from __future__ import annotations

from typing import Type, Callable, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from Client import Client

E = TypeVar('E', bound='Event')


class EventHandler(Generic[E]):
    def __init__(self, event_type: Type[E], event_callback: Callable[[Client, E], None]):
        self.event_type = event_type
        self.callback = event_callback
