import uuid, requests
from django.db import models
from django.utils import timezone
from signals import request_done, request_failed

class Request(models.Model):
  NEW, RUNNING, RETRYING, FAILED, READY = range(5)
  STATUS = [
    (NEW, "New"),
    (RUNNING, "Running"),
    (RETRYING, "Retrying"),
    (FAILED, "Failed"),
    (READY, "Ready"),
  ]


  uuid = models.CharField(verbose_name='UUID', max_length = 127, default = uuid.uuid4)
  url = models.URLField(verbose_name='URL')
  max_retries = models.PositiveIntegerField(default = 3)
  retries = models.PositiveIntegerField(default = 0)
  last_try = models.DateTimeField(null = True, blank = True)
  status = models.PositiveIntegerField(choices = STATUS, default = NEW)

  comment = models.TextField(blank = True)

  def run(self):
    if self.status in [Request.READY, Request.FAILED]: return
    self.status = Request.RUNNING
    self.last_try = timezone.now()
    self.save()

    try:
      response = requests.get(self.url)
      response.raise_for_status()
    except Exception, e:
      self.comment += str(e) + "\n"
      self.retries += 1
      self.status = Request.FAILED if self.retries >= self.max_retries else Request.RETRYING
      request_failed.send(sender = Request, instance = self, response = response, error = e)
    else:
      self.status = Request.READY
      request_done.send(sender = Request, instance = self, response = response)
    finally:
      self.save()
