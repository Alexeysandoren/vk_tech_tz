from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import Friends


@receiver(pre_save, sender=Friends)
def confirm_both_applications(sender, instance, **kwargs):
    if instance.pk is None:
        opposite_request = Friends.objects.filter(
            friend_request_receiver=instance.friend_request_sender,
            friend_request_sender=instance.friend_request_receiver
        ).first()
        if opposite_request:
            instance.application_status = Friends.APPLICATION_STATUS.APPROVED
            opposite_request.application_status = (
                Friends.APPLICATION_STATUS.APPROVED)
            opposite_request.save()


@receiver(post_delete, sender=Friends)
def delete_friends(sender, instance, **kwargs):
    Friends.objects.filter(
        friend_request_receiver=instance.friend_request_sender,
        friend_request_sender=instance.friend_request_receiver
    ).delete()
