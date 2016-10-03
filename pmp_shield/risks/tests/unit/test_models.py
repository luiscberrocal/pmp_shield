from django.test import TestCase

from ...models import Risk
from ..factories import RiskFactory


class TestRisk(TestCase):

    def test_create(self):
        risk = RiskFactory.create()
        self.assertEqual(1, Risk.objects.count())
