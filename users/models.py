from django.db.models.deletion       import CASCADE
from django.db.models.fields         import CharField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from restaurants.models              import Restaurant
from mangoPeace.common               import TimeStampModel
from users.validation                import validate_email, validate_nickname, validate_password, validate_phone_number

class User(TimeStampModel):
    nick_name            = CharField(max_length=15, unique=True)
    email                = CharField(max_length=200, unique=True)
    password             = CharField(max_length=200)
    phone_number         = CharField(max_length=20, unique=True, null=True)
    profile_url          = URLField(null=True)
    wishlist_restaurants = ManyToManyField(Restaurant, through="Wishlist", related_name="wishlist_user")
    reviewed_restaurants = ManyToManyField(Restaurant, through="Review", related_name="reviewed_user")

    @classmethod
    def validate(cls, data):
        if not validate_email(data["email"]):
            return False
        
        if not validate_nickname(data["nickname"]):
            return False
        
        if not validate_password(data["password"]):
            return False
        
        if not validate_phone_number(data["phone_number"]):
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