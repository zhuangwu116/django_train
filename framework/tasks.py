from __future__ import absolute_import,unicode_literals
from celery import shared_task
import httplib2
@shared_task
def request_http(url):
    h = httplib2.Http(".cache")
    resp_headers,content = h.request(url,"GET")
    return resp_headers,content