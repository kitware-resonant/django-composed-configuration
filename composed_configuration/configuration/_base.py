from typing import Type

from configurations import Configuration, values

# With the default "late_binding=False", and "environ_name" is specified or "environ=False",
# even Values from non-included classes (e.g. `AWS_DEFAULT_REGION) get immediately evaluated and
# expect env vars to be set. Also, immediately evaluated Values cannot be tweaked effectively
# in "before_binding").
values.Value.late_binding = True


class ComposedConfiguration(Configuration):
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
            # If the class has "before_binding" as its own (non-inherited) method
            if 'before_binding' in base_cls.__dict__:
                base_cls.before_binding(cls)


class ConfigMixin:
    """Abstract mixin for composable Config sections."""

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        """
        Run before values are fully bound with environment variables.

        `configuration` refers to the final Configuration class, so settings from
        other Configs in the final hierarchy may be referenced.
        """
        pass
