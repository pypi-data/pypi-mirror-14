import factory

from .. import models


class SpeakerFactory(factory.DjangoModelFactory):
    name = factory.Sequence('Speaker {}'.format)
    slug = factory.Sequence('speaker-{}'.format)

    class Meta:
        model = models.Speaker
