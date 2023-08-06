from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
import timeside.core
from timeside.server.models import *
from timeside.core.tools.test_samples import generateSamples
from telemeta.models import *


class Command(BaseCommand):
    help = "Setup and run a boilerplate for testing"
    cleanup =  True
    code = 'Tests'

    def processor_cleanup(self):
        for processor in Processor.objects.all():
            processor.delete()

    def result_cleanup(self):
        for result in Result.objects.all():
            result.delete()

    def handle(self, *args, **options):
        collection, c = MediaCollection.objects.get_or_create(title=self.code,
                            code=self.code)
        selection, c = Selection.objects.get_or_create(title='Tests')

        if c:
            presets = []
            blacklist =['decoder', 'live', 'gain', 'vamp']
            processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
            for proc in processors:
                trig = True
                for black in blacklist:
                    if black in proc.id():
                        trig = False
                if trig:
                    processor, c = Processor.objects.get_or_create(pid=proc.id())
                    preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
                    presets.append(preset)

            media_dir = 'items' + os.sep + 'tests'
            samples_dir = settings.MEDIA_ROOT + media_dir
            samples = generateSamples(samples_dir=samples_dir)

            for sample in samples.iteritems():
                filename, path = sample
                title = os.path.splitext(filename)[0]
                path = media_dir + os.sep + filename
                item, c = Item.objects.get_or_create(title=title, file=path)
                if not item in selection.items.all():
                    selection.items.add(item)
                if self.cleanup:
                    for result in item.results.all():
                        result.delete()
                mediaitem, c = MediaItem.objects.get_or_create(title=title,
                                    code=self.code + '-' + slugify(filename),
                                    file=path, collection=collection)


            experience, c = Experience.objects.get_or_create(title='All')
            for preset in presets:
                if not preset in experience.presets.all():
                    experience.presets.add(preset)

            task = Task(experience=experience, selection=selection)
            task.save()
