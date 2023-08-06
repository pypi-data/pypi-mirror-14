from celery.task import task

from django.apps import apps


@task(name='c.unittest.SomeAppTask')
def SomeAppTask(**kwargs):
    return 42


@task(name='c.unittest.SomeModelTask')
def SomeModelTask(pk):
    model = apps.get_model('someapp', 'Thing')
    thing = model.objects.get(pk=pk)
    return thing.name
