from .activity import activity_emojis 
from .flags import flags_emojis
from .food import food_emojis
from .nature import nature_emojis
from .objects import objects_emojis
from .people import people_emojis
from .symbols import symbols_emojis
from .travel import travel_emojis

__all__ = ("emojis")

emojis = {
    **activity_emojis,
    **flags_emojis,
    **food_emojis,
    **nature_emojis,
    **objects_emojis,
    **people_emojis,
    **symbols_emojis,
    **travel_emojis
}