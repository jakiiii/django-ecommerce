# Custom signals
from django.dispatch import Signal


object_viewed_signals = Signal(providing_args=['instance', 'request'])
