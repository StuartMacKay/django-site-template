from django.test import TestCase

import pytest

from project.tests.factories import UserFactory
from project.tests.mixins import AdminTests

pytestmark = pytest.mark.django_db


class UserAdminTests(AdminTests, TestCase):
    factory_class = UserFactory
    query_count = 7
