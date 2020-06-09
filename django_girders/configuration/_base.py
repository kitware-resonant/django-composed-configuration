from typing import Type

from configurations import Configuration, values


# When "environ_name" is specified or "environ=False", a Value will immediately bind (and so
# cannot be tweaked effectively in "before_binding"), unless "late_binding=True"
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

    @classmethod
    def post_setup(cls):
        super().post_setup()

        for base_cls in reversed(cls.__mro__):
            if 'after_binding' in base_cls.__dict__:
                base_cls.after_binding(cls)


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

    @staticmethod
    def after_binding(configuration: Type[ComposedConfiguration]) -> None:
        """
        Run after values are fully bound with environment variables.

        `configuration` refers to the final Configuration class, so settings from
        other Configs in the final hierarchy may be referenced.
        """
        pass
