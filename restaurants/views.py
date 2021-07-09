import json
import jwt

from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.utils import timezone

from users.utils import ConfirmUser
from users.models import Review, User
from restaurants.models import Food, Image, Restaurant

class RestaurantView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)

            restaurant = {
                "id":restaurant_instance.id,
                "sub_category": restaurant_instance.sub_category.name,
                "name": restaurant_instance.name,
                "address": restaurant_instance.address,
                "phone_number": restaurant_instance.phone_number,
                "coordinate": restaurant_instance.coordinate,
                "open_time": restaurant_instance.open_time,
                "updated_at": restaurant_instance.updated_at,
            }

            return JsonResponse({"message":"success", "result":restaurant}, status=200)
        
        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":e}, status=400)

class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods = []
            foods_queryset = Restaurant.objects.get(id=restaurant_id).food_set.all()
            
            for food_instance in foods_queryset:
                images = []
                images_queryset = Image.objects.filter(food=food_instance)
                for image_instance in images_queryset:
                    images.append(image_instance.image_url)
                food = {
                    "id":food_instance.id,
                    "name":food_instance.name,
                    "price":food_instance.price,
                    "images":images,
                }
                foods.append(food)
            
            return JsonResponse({"message":"success", "result":foods}, status=200)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":e}, status=400)

class RestaurantReviewView(View):
    def get(self, request, restaurant_id):
        try:
            reviews = []
            reviews_queryset = Restaurant.objects.get(id=restaurant_id).review_set.all()
            
            for r in reviews_queryset:
                print(type(r.id))
                print(type(r.rating))
                review = {
                    "user":{
                        "id":r.user.id,
                        "full_name":r.user.full_name,
                        "profile_image":r.user.profile_url if hasattr(r.user, "profile_url") else None,
                        # 리뷰 갯수
                        # ? 아무튼 갯수. 친구수인가 스토리 수인가. 
                    },
                    "id":r.id,
                    "content" : r.content,
                    "rating":r.rating,
                    "created_at":r.created_at,
                }
                reviews.append(review)

            return JsonResponse({"message":"success", "result":reviews}, status=200)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":e}, status=400)

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
            # token에 대한 유저
            # user_instance = request.user
            user_instance = User.objects.get(id=1)
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            is_wished = user_instance.wishlist_restaurants.filter(id=restaurant_id).exists()

            if is_wished:
                user_instance.wishlist_restaurants.remove(restaurant_instance)
                status_code = 200
            else:
                user_instance.wishlist_restaurants.add(restaurant_instance)
                status_code = 201

            return JsonResponse({"message":"success"}, status=status_code)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
