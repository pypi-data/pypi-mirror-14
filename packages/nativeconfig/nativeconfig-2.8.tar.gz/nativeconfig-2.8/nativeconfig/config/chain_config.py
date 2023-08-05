"""
Set of decorators that allow one to chain same config file from multiple locations.

This is useful, when something may can configured on different level of access.
Typical example is when you have some global config that can be overridden my local configs (.gitconfig)
or when some global config set by administrator should override any user values.
"""

def chain(config_cls, **kwargs):
    pass