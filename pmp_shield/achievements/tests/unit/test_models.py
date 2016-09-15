from django.test import TestCase

from ...models import Achievement
from ..factories import AchievementFactory


class TestAchievement(TestCase):

    def test_create(self):
        AchievementFactory.create()
        self.assertEqual(1, Achievement.objects.count())
