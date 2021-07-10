import re

from django.db.models.deletion       import CASCADE
from django.db.models.fields         import CharField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from restaurants.models              import Restaurant
from mangoPeace.common               import TimeStampModel

NICKNAME_REGEX     = r'^[a-zA-Z가-힇0-9]{1,8}$'
EMAIL_REGEX        = r'^[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$'
PASSWORD_REGEX     = r'^(?=.+[a-z])(?=.+[A-Z])(?=.+\d)(?=.+[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=,./<>?]{6,25}$'
PHONE_NUMBER_REGEX = r'^01[1|2|5|7|8|9|0][0-9]{3,4}[0-9]{4}$'

class User(TimeStampModel):
    nickname             = CharField(max_length=15, unique=True)
    email                = CharField(max_length=200, unique=True)
    password             = CharField(max_length=200)
    phone_number         = CharField(max_length=20, unique=True, null=True)
    profile_url          = URLField(null=True)
    wishlist_restaurants = ManyToManyField(Restaurant, through="Wishlist", related_name="wishlist_user")
    reviewed_restaurants = ManyToManyField(Restaurant, through="Review", related_name="reviewed_user")

    @classmethod
    def validate(cls, data):
        if not re.match(EMAIL_REGEX, data["email"]):
            return False
        
        if not re.match(NICKNAME_REGEX, data["nickname"]):
            return False
        
        if not re.match(PASSWORD_REGEX, data["password"]):
            return False
        
        if not re.match(PHONE_NUMBER_REGEX, data["phone_number"]):
            return False
        
        return True

    class Meta():
        db_table = "users"

class Wishlist(TimeStampModel):
    user       = ForeignKey(User, on_delete=CASCADE)
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE)

    class Meta():
        db_table        = "wishlists"
        unique_together = ['user', 'restaurant']

class Review(TimeStampModel):
    user       = ForeignKey(User, on_delete=CASCADE)
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE)
    content    = TextField()
    rating     = IntegerField(max_length=1)

    class Meta():
        db_table = "reviews"