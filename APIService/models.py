from django.db import models


class RepairRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    linenos = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
