from django.db.models.deletion       import CASCADE
from django.db.models.fields         import CharField, DateTimeField, DecimalField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from restaurants.models              import Restaurant
from mangoPeace.common               import TimeStampModel

class User(TimeStampModel):
    full_name            = CharField(max_length=45)
    email                = CharField(max_length=200, unique=True)
    password             = CharField(max_length=200)
    phone_number         = CharField(max_length=20, unique=True, null=True)
    profile_url          = URLField(null=True)
    wishlist_restaurants = ManyToManyField(Restaurant, through="Wishlist", related_name="wishlist_user")
    reviewed_restaurants = ManyToManyField(Restaurant, through="Review", related_name="reviewed_user")

    class Meta():
        db_table = "users"

class Wishlist(TimeStampModel):
    user                = ForeignKey(User, on_delete=CASCADE)
    restaurant          = ForeignKey(Restaurant, on_delete=CASCADE)

    class Meta():
        db_table        = "wishlists"
        unique_together = ['user', 'restaurant']

class Review(TimeStampModel):
    user                = ForeignKey(User, on_delete=CASCADE)
    restaurant          = ForeignKey(Restaurant, on_delete=CASCADE)
    content             = TextField()
    rating              = DecimalField(max_digits=2, decimal_places=1)

    class Meta():
        db_table = "reviews"