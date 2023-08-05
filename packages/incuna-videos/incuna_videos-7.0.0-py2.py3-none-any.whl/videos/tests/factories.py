import factory

from .. import models


class SourceFactory(factory.DjangoModelFactory):
    file = 'randomfile.mp4'
    type = models.Source.TYPE_MP4  # An arbitrary default for the factory
    video = factory.SubFactory('videos.tests.factories.VideoFactory')

    class Meta:
        model = models.Source


class VideoFactory(factory.DjangoModelFactory):
    title = factory.Sequence('Video {}'.format)
    slug = factory.Sequence('video-{}'.format)
    captions_file = 'captionfile.txt'
    preview = factory.django.FileField(from_path='videos/tests/files/image.png')

    class Meta:
        model = models.Video
