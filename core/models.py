from cms.models import CMSPlugin
from django.db import models


class HeroTitle(CMSPlugin):
    text = models.CharField(max_length=255, help_text="Main heading for the page.")

    def __str__(self):
        return self.text
