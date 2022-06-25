import os
from uuid import uuid4

from PIL import Image
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from resizeimage import resizeimage


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.id, ext)  # do instance.username
        # if you want to save as username
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # filename = '{}.{}'.format(instance.id, ext)  # do instance.username
    # return the whole path to the file
    return os.path.join('profile_images', filename)


class Profile(models.Model):
    boolChoice = (
        ("M", "Male"), ("F", "Female"), ("O", "Other")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=25, blank=True, null=True)

    # PHONE_NUMBER_REGEX = RegexValidator(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[6789]\d{9}$',
    #                                     'Mobile Number Not Valid')
    PHONE_NUMBER_REGEX = RegexValidator(r'^[6-9]\d{9}$',
                                        'Mobile Number Not Valid')
    phone = models.CharField(max_length=10, validators=[PHONE_NUMBER_REGEX], blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    dob = models.DateField(max_length=8, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=boolChoice, blank=True, null=True)

    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    avatar = models.ImageField(default='default.jpg', upload_to=wrapper)

    bio = models.TextField(blank=True, null=True)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            # new_img = (100, 100)
            new_img = (img.width, img.height)
            img.thumbnail(new_img)

            img.save(self.avatar.path)


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
