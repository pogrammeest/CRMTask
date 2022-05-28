from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

statuses = [
    ('Открыта', 'Открыта'),
    ('В работе', 'В работе'),
    ('Закрыта', 'Закрыта'),
]


@receiver(pre_save, sender=User)
def on_change(sender, instance: User, **kwargs):
    if instance.id:
        previous = User.objects.get(id=instance.id)
        if previous.is_staff != instance.is_staff:  # field will be updated
            if instance.is_staff:
                UserDetails.objects.filter(user=instance).delete()
                Staff.objects.create(user=instance)
            else:
                Staff.objects.filter(user=instance).delete()
                UserDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def on_create(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            Staff.objects.create(user=instance)
        else:
            UserDetails.objects.create(user=instance)


class UserDetails(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Staff(models.Model):
    user = models.OneToOneField(User, related_name='staff', on_delete=models.CASCADE)
    experiences = models.IntegerField(default='1')

    def __str__(self):
        return self.user.username


class RepairRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('UserDetails', related_name='repair_request', on_delete=models.CASCADE, null=True,
                              blank=False)
    responsible = models.ForeignKey('Staff', related_name='repair_tasks', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=statuses, default='открыта', max_length=100)

    class Meta:
        ordering = ['created']
