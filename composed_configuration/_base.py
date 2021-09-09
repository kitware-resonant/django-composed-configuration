from typing import Type
import warnings

from configurations import Configuration, values
from configurations.base import ConfigurationBase

# With the default "late_binding=False", and "environ_name" is specified or "environ=False",
# even Values from non-included classes (e.g. `AWS_DEFAULT_REGION) get immediately evaluated and
# expect env vars to be set. Also, immediately evaluated Values cannot be tweaked effectively
# in "mutate_configuration").
values.Value.late_binding = True


# Fix https://github.com/jazzband/django-configurations/issues/263
# Since this attribute is set by the metaclass, it exists on the already-instantied Configuration
# class. It also will be re-set on every subclass, but since those are not instantied yet, we
# can replace the metaclass for all subclasses with a fixed one.
try:
    del Configuration.DEFAULT_HASHING_ALGORITHM
except AttributeError:
    pass


class FixedConfigurationBase(ConfigurationBase):
    def __new__(cls, name, bases, attrs):
        obj = super().__new__(cls, name, bases, attrs)
        try:
            del obj.DEFAULT_HASHING_ALGORITHM
        except AttributeError:
            pass
        return obj


class ComposedConfiguration(Configuration, metaclass=FixedConfigurationBase):
    """
    Abstract base for composed Configuration.

    This must always be specified as a base class after Config mixins.
    """

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

        # For every class in the inheritance hierarchy
        # Reverse order allows more base classes to run first
        for base_cls in reversed(cls.__mro__):
            # If the class has "mutate_configuration" as its own (non-inherited) method
            if 'mutate_configuration' in base_cls.__dict__:
                base_cls.mutate_configuration(cls)
            elif 'before_binding' in base_cls.__dict__:
                warnings.warn(
                    'In "ConfigMixin" subclasses, '
                    '"before_binding" should be renamed to "mutate_configuration"',
                    DeprecationWarning,
                )
                base_cls.before_binding(cls)


class ConfigMixin:
    """Abstract mixin for composable Config sections."""

    @staticmethod
    def mutate_configuration(configuration: Type[ComposedConfiguration]) -> None:
        """
        Mutate the configuration before values are fully bound with environment variables.

        `configuration` refers to the final Configuration class, so settings from
        other Configs in the final hierarchy may be referenced.
        """
        pass
