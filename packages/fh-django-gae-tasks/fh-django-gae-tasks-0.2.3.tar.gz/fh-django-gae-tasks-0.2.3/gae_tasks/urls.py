from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

import tasks

urlpatterns = [
    url(r'^_cb/deferred/(?P<module>.+)/(?P<name>.+)', csrf_exempt(tasks.DeferredView.as_view())),
]
