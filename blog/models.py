from django.db import models
from django.conf import settings

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        ordering = ('tag',)

    def __str__(self):
        return self.tag

class Theme(models.Model):
    """docstring for Subject"""
    """ Subject """
    name = models.CharField(max_length=30)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    """docstring for Content"""
    """ Content """
    file = models.FileField(upload_to='contents/%Y/%m/')
    address = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    taken_dt = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.url

class Post(models.Model):
    """docstring for Post"""
    """ 설명 """
    theme = models.ForeignKey(Theme, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(default=0, blank=True, null=True)
    lng = models.FloatField(default=0, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_dt = models.DateTimeField(auto_now_add=True)
    contents = models.ManyToManyField(Content)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('-id',)





# class Post(models.Model):
#     """ Picture/Clip/Article """
#     TEXT = 'T'
#     PHOTO ='P'
#     CLIP = 'M'
#     CONTENT_CHOICES = (
#         (TEXT, _('Text')),
#         (PHOTO, _('Photo')),
#         (CLIP, _('Clip')),
#     )
#     cont_type = models.CharField(max_length=1, choices=CONTENT_CHOICES, default=PHOTO)
#     cont_file = models.FileField(null=True, blank=True)
#     article = models.TextField(null=True, blank=True)
#     # taken_pos = models.PointField(null=True, blank=True)
#     # write_pos = models.PointField(null=True, blank=True)
#     likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
#     following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')
#     create_user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)


# from openpyxl import load_workbook
# import pandas as pd
# def read_person_data():

#     wb = load_workbook('person.xlsx')
#     ws = wb['Sheet']
#     df = pd.DataFrame(ws.values)

#     for index, row in df.iterrows():
#         if index == 0:
#             continue
#         print(row)
#         email = row[0]
#         passwd = row[1]
#         name = row[2]
#         birth = row[3]
#         num = row[4]
#         friends = row[5]

#         user, created = User.objects.get_or_create(username=email, first_name=name, email=email)
#         user.set_password(passwd)
#         # 사진 입력

#         person, created = Person.objects.get_or_create(user=user, birthdate=birth, num=num)

#         if friends:
#             friends = friends.strip()
#             friend_list = friends.split(',')
#             for friend in friend_list:
#                 obj = Person.objects.get(num=friend)
#                 print(obj.user.first_name)
#                 person.friends.add(obj)
#                 obj.friends.add(person)




# from openpyxl import load_workbook
# import pandas as pd
# from django.contrib.auth import get_user_model
# def read_post_data():

#     User = get_user_model()
#     wb = load_workbook('positions.xlsx')
#     ws = wb['Sheet']
#     df = pd.DataFrame(ws.values)

#     for index, row in df.iterrows():
#         if index == 0:
#             continue
#         print(row)
#         name = row[0]
#         address = row[1]
#         lat = row[2]
#         lng = row[3]
#         picture = row[4]
#         user = row[5]

#         user = User.objects.get(id=user)
#         post= Post.objects.create(name=name, address=address, lat=lat,
#                 lng=lng, picture=picture, create_user=user)
#         print(post)