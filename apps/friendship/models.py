from classes.base_model import BaseModel

from django.db import models

class Friendship(BaseModel):
    CHOICES = (
        ('PENDING', 'PENDING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('DECLINED', 'DECLINED'),
        ('BLOCKED', 'BLOCKED'),
    )
    # chat_id = models.ForeignKey()
    from_user = models.ForeignKey(
        'user.UserProfile', on_delete=models.CASCADE, related_name='sent_requests'
        )
    to_user = models.ForeignKey(
        'user.UserProfile', on_delete=models.CASCADE, related_name='received_requests'
        )
    status = models.CharField(choices=CHOICES, default='PENDING')

    # class Meta:
    #     unique_together = ('from_user', 'to_user')
