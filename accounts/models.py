from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Profile(models.Model):
    """docstring for Person"""
    """ 기억할 인물에 대한 설명 """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    birthdate = models.DateTimeField(_('Birth Date'), null=True, blank=True)
    picture = models.ImageField(_('Profile Picture'), upload_to='person_profile/%Y/%m/',
                     null=True, blank=True)
    friends = models.ManyToManyField('self', related_name='friends')
    num = models.IntegerField(_('UID'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    def friend_list(self):
        friends = self.friends.all()
        html = ''
        for friend in friends:
            html = "{} {}".format(html, friend.user)

        return html


    # def notify_person_liked(self, person):
    #     if self.user != person.created_user:
    #         Notification(notification_type=Notification.LIKED, 
    #             from_user=self.user, to_user=person.created_user,
    #             person=person).save()

    # def notify_person_unliked(self, person):
    #     if self.user != person.created_user:
    #         Notification.objects.filter(notification_type=Notification.LIKED,
    #             from_user=self.user, to_user=person.created_user,person=person).delete()

    # def notify_person_commented(self, person):
    #     if self.user != person.created_user:
    #         Notification(notification_type=Notification.COMMENTED, 
    #             from_user=self.user, to_user=person.created_user,
    #             person=person).save()

    # def notify_person_following(self, person):
    #     if self.user != person.created_user:
    #         Notification(notification_type=Notification.FOLLOWING, 
    #             from_user=self.user, to_user=person.created_user,
    #             person=person).save()

    # def notify_person_unfollowing(self, person):
    #     if self.user != person.created_user:
    #         Notification.objects.filter(notification_type=Notification.FOLLOWING,
    #             from_user=self.user, to_user=person.created_user,person=person).delete()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)