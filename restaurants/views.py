import json
import jwt

from json.decoder import JSONDecodeError
from decimal      import Decimal

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.utils import timezone
from django.db.models import Avg

from users.utils import ConfirmUser, YameConfirmUser
from users.models import Review, User
from restaurants.models import Food, Image, Restaurant

class RestaurantDetailView(View):
    @YameConfirmUser
    def get(self, request, restaurant_id):
        try:
            restaurant     = Restaurant.objects.get(id=restaurant_id)
            if not request.user:
                
            # 임시 유저
            user           = User.objects.get(id=1)
            is_wished      = user.wishlist_restaurants.filter(id=restaurant_id).exists()
            average_price  = Food.objects.filter(restaurant_id=restaurant.id).aggregate(Avg("price"))["price__avg"]
            reviews        = restaurant.review_set.all()
            average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] if reviews.exists() else 0
            review_count   = {
                "total"        : reviews.count(),
                "rating_one"   : reviews.filter(rating=1).count(),
                "rating_two"   : reviews.filter(rating=2).count(),
                "rating_three" : reviews.filter(rating=3).count(),
                "rating_four"  : reviews.filter(rating=4).count(),
                "rating_five"  : reviews.filter(rating=5).count(),
            }

            result = {
            "id"             : restaurant.id,
            "sub_category"   : restaurant.sub_category.name,
            "name"           : restaurant.name,
            "address"        : restaurant.address,
            "phone_number"   : restaurant.phone_number,
            "coordinate"     : restaurant.coordinate,
            "open_time"      : restaurant.open_time,
            "updated_at"     : restaurant.updated_at,
            "average_price"  : average_price,
            "is_wished"      : is_wished,
            "review_count"   : review_count,
            "average_rating" : average_rating,
            }

            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

class RestaurantFoodsView(View):
    def get(self, request, restaurant_id):
        try:
            foods      = Food.objects.filter(restaurant_id=restaurant_id)
            foods_list = [{"id":f.id, "name":f.name, "price":f.price, "images":[i.image_url for i in f.images.all()]} for f in foods]

            return JsonResponse({"message":"success", "result":foods_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404) 

class RestaurantFoodImageView(View):
    def get(self, request, restaurant_id):
        try:
            foods      = Restaurant.objects.get(id=restaurant_id).foods.all()
            image_list = []

            for f in foods:
                images = Image.objects.filter(food=f)
                
                for i in images:
                    image_list.append(i.image_url)
            
            return JsonResponse({"message":"success", "result":image_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

class RestaurantReviewView(View):
    def get(self, request, restaurant_id):
        offset        = int(request.GET.get("offset", 0))
        limit         = int(request.GET.get("limit", 10))
        rating_min    = request.GET.get("rating-min", 1)
        rating_max    = request.GET.get("rating-max", 5)
        reviews       = Review.objects.filter(restaurant_id=restaurant_id, rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[offset : offset + limit]
        review_list   = [{
                "user":{
                    "id":r.user.id,
                    "nickname":r.user.nickname,
                    "profile_image":r.user.profile_url,
                    "review_count":r.user.reviewed_restaurants.count()
                },
                "id":r.id,
                "content" : r.content,
                "rating":r.rating,
                "created_at":r.created_at,
            } for r in reviews]

        return JsonResponse({"message":"success", "result":review_list}, status=200)

    # @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            # token에 대한 유저
            # user_instance = request.user
            user_instance = User.objects.get(id=1)
            restaurant = Restaurant.objects.get(id=restaurant_id)
            content = data["content"]
            rating = data["rating"]

            Review.objects.create(
                user=user_instance,
                restaurant=restaurant,
                content = content,
                rating=rating
            )

            return JsonResponse({"message":"success"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)
    
class ReviewView(View):
    # @ConfirmUser
    def patch(self, request, restaurant_id, review_id):
        try:
            data    = json.loads(request.body)
            content = data["content"]
            rating  = data["rating"]
            reviews = Review.objects.filter(id=review_id)
            
            print(content, rating, reviews)
            reviews.update(content=content, rating=rating, updated_at=timezone.now())

            return JsonResponse({"message":"success"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

    # @ConfirmUser
    def delete(self, request, restaurant_id, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()

            return JsonResponse({"message":"success"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)



        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)


class WishListView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            print(request.user)
            print(request.user.id)
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_ALREADY_EXISTS"}, status=400)

            request.user.wishlist_restaurants.add(restaurant)
            
            return JsonResponse({"message":"success"}, status=201)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)   
        
    @ConfirmUser
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if not request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_NOT_EXISTS"}, status=404)
           
            request.user.wishlist_restaurants.remove(restaurant)

            return JsonResponse({"message":"success"}, status=204)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)