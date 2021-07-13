import json
import jwt

from json.decoder import JSONDecodeError
from decimal      import Decimal

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.utils import timezone
from django.db.models import Avg

from users.utils import ConfirmUser
from users.models import Review, User
from restaurants.models import Food, Image, Restaurant

class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            fake_user_instance  = User.objects.get(id=1)
            is_wished           = fake_user_instance.wishlist_restaurants.filter(id=restaurant_id).exists()

            reviews                   = restaurant_instance.review_set.all()
            average_rating            = reviews.aggregate(Avg("rating"))["rating__avg"] if reviews.exists() else 0
            review_total_count        = reviews.count()
            review_rating_one_count   = reviews.filter(rating=1).count()
            review_rating_two_count   = reviews.filter(rating=2).count()
            review_rating_three_count = reviews.filter(rating=3).count()
            review_rating_four_count  = reviews.filter(rating=4).count()
            review_rating_five_count  = reviews.filter(rating=5).count()

            review_count = {
                "total" : review_total_count,
                "rating_one" : review_rating_one_count,
                "rating_two" : review_rating_two_count,
                "rating_three" : review_rating_three_count,
                "rating_four" : review_rating_four_count,
                "rating_five" : review_rating_five_count,
            }
            result = {
            "id":restaurant_instance.id,
            "sub_category": restaurant_instance.sub_category.name,
            "name": restaurant_instance.name,
            "address": restaurant_instance.address,
            "phone_number": restaurant_instance.phone_number,
            "coordinate": restaurant_instance.coordinate,
            "open_time": restaurant_instance.open_time,
            "updated_at": restaurant_instance.updated_at,
            "is_wished" : is_wished,
            "review_count" : review_count,
            "average_rating" : average_rating,
        }
            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)
        
        
class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods = []
            foods_queryset = Restaurant.objects.get(id=restaurant_id).foods.all()
            
            for food_instance in foods_queryset:
                food = {
                    "id":food_instance.id,
                    "name":food_instance.name,
                    "price":food_instance.price,
                }
                foods.append(food)
            
            return JsonResponse({"message":"success", "result":foods}, status=200)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

class RestaurantFoodImageView(View):
    def get(self, request, restaurant_id):
        try:
            foods  = Restaurant.objects.get(id=restaurant_id).foods.all()
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
        try:
            UNIT_PER_PAGE = 10
            limit         = int(request.GET.get("limit", 1)) * UNIT_PER_PAGE
            rating_min    = request.GET.get("rating-min", 0)
            rating_max    = request.GET.get("rating-max", 5)
            
            restaurant  = Restaurant.objects.get(id=restaurant_id)
            reviews     = restaurant.review_set.filter(rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[limit - UNIT_PER_PAGE : limit]
            review_list = []

            for r in reviews:
                review = {
                    "user":{
                        "id":r.user.id,
                        "nickname":r.user.nickname,
                        "profile_image":r.user.profile_url if hasattr(r.user, "profile_url") else None,
                    },
                    "id":r.id,
                    "content" : r.content,
                    "rating":r.rating,
                    "created_at":r.created_at,
                }
                review_list.append(review)

            return JsonResponse({"message":"success", "result":review_list}, status=200)

        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status=400)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)


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
            data = json.loads(request.body)
            content = data["content"]
            rating = data["rating"]
            review_queryset = Review.objects.filter(id=review_id)
            
            review_queryset.update(content=content, rating=rating, updated_at=timezone.now())

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
            restaurant = Restaurant.objects.get(id=restaurant_id)
            print(restaurant)
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
            print(restaurant)
            if not request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_NOT_EXISTS"}, status=404)

            request.user.wishlist_restaurants.remove(restaurant)

            return JsonResponse({"message":"success"}, status=204)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404) 