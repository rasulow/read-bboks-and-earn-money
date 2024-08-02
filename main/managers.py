from django.db import models
from utils.words import get_random_word


class PurchaseManager(models.Manager):
    def create(self, *args, **kwargs):
        random_word = get_random_word()
        kwargs['word'] = random_word
        kwargs['testing_word'] = random_word
        return super().create(*args, **kwargs)