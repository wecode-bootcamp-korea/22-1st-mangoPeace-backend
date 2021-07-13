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
            print(restaurant_id)
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            fake_user_instance  = User.objects.get(id=1)
            is_wished           = fake_user_instance.wishlist_restaurants.filter(id=restaurant_id).exists()

            reviews_queryset          = restaurant_instance.review_set.all()
            average_rating            = reviews_queryset.aggregate(Avg("rating"))["rating__avg"]
            review_total_count        = reviews_queryset.count()

            review_rating_one_count   = reviews_queryset.filter(rating=1).count()
            review_rating_two_count   = reviews_queryset.filter(rating=2).count()
            review_rating_three_count = reviews_queryset.filter(rating=3).count()
            review_rating_four_count  = reviews_queryset.filter(rating=4).count()
            review_rating_five_count  = reviews_queryset.filter(rating=5).count()

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
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=400)        
        
        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
        
        
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
            
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            
            reviews_queryset = restaurant_instance.review_set
            # 평점순 -> 생성일자순 -> limit
            filtered = reviews_queryset.filter(rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[limit - UNIT_PER_PAGE : limit]
            reviews  = []

            for review_instance in filtered:
                review = {
                    "user":{
                        "id":review_instance.user.id,
                        "nickname":review_instance.user.nickname,
                        "profile_image":review_instance.user.profile_url if hasattr(review_instance.user, "profile_url") else None,
                        # "review_count":review_instance.user.reviewed_restaurants.count()
                    },
                    "id":review_instance.id,
                    "content" : review_instance.content,
                    "rating":review_instance.rating,
                    "created_at":review_instance.created_at,
                }
                reviews.append(review)

            return JsonResponse({"message":"success", "result":reviews}, status=200)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

    # @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            # token에 대한 유저
            # user_instance = request.user
            user_instance = User.objects.get(id=1)
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            content = data["content"]
            rating = data["rating"]

            Review.objects.create(
                user=user_instance,
                restaurant=restaurant_instance,
                content = content,
                rating=rating
            )

            return JsonResponse({"message":"success"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
    
    # @ConfirmUser
    def patch(self, request, review_id):
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

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

    # @ConfirmUser
    def delete(self, request, review_id):
        try:
            review_instance = Review.objects.get(id=review_id)
            
            review_instance.delete()

            return JsonResponse({"message":"success"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

class WishListView(View):
    # @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            print(request)
            # token에 대한 유저
            # user_instance = request.user
            # 1. 1번 유저
            user_instance = User.objects.get(id=1)
            # 2. 레스토랑 가져오기
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            # 3. DB에 없으면, 추가.
            if not user_instance.wishlist_restaurants.all().exists():
                user_instance.wishlist_restaurants.add(restaurant_instance)
            # 이미 있으면, 에러 던짐
            else:
                return JsonResponse({"message":"ALREADY_EXISTS"}, status=400)
            
            # 4. 정상 : success 
            return JsonResponse({"message":"success"}, status=201)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

    def delete(self, request, restaurant_id):
        try:
            print(request)
            # token에 대한 유저
            # user_instance = request.user
            user_instance = User.objects.get(id=1)
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            if user_instance.wishlist_restaurants.all().exists():
                user_instance.wishlist_restaurants.remove(restaurant_instance)
            # 없는데 delete를 할ㄹ라고 한다? 너 나빴어!
            else:
                return JsonResponse({"message":"NOT_EXISTS"}, status=400)
            # 정상 : success    
            return JsonResponse({"message":"success"}, status=204)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
