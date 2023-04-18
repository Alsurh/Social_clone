from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Smeep(models.Model):
    user = models.ForeignKey(
        User, related_name="smeep",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )


# Creat A User Profile Model
class Profile(models.Model):
    # One User can have only one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # One user can have many followers
    follows = models.ManyToManyField("self",
                                     related_name='followed_by',
                                     symmetrical=False,
                                     blank=True)

    date_modified = models.DateTimeField(User,auto_now=True)
    profile_image = models.ImageField(null=True, blank = True, upload_to='images')

    def __str__(self):
        return self.user.username


# Create Profile when New User Signs Up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)