# import factory  # type: ignore

# from project.tests.providers import html

from .user import UserFactory

__all__ = [
    "UserFactory",
]

# Register the custom providers here, so they are available anywhere
# the factories are used. This could be added to the root conftest.py,
# but we occasionally want to be able to create instances of factories
# in the django shell, particularly for ad-hoc testing.

# factory.Faker.add_provider(...)
