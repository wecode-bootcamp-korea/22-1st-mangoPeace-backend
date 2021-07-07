import json
import jwt

from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError

from users.utils import ConfirmUser
from users.models import Review
from restaurants.models import Food, Image, Restaurant

# ? : restaurant 생성 로직. 사이트에서 누군가는 Restaurant를 생성해야 하지 않을까? 최소한 관리자는.
# ? : review의 유저정보에는 그 유저가 쓴 리뷰의 갯수와 이름 모를 게 하나 있다.
# ? : image. image의 url만 넣으면 끝인건가?

class RestaurantView(View):
    def get(self, request, restaurant_id):
        restaurant_instance = Restaurant.objects.get(id=restaurant_id)
        
        foods = []
        foods_queryset = Food.objects.filter(restaurant=restaurant_instance)
        
        for food_instance in foods_queryset:
            images = []
            images_queryset = Image.objects.filter(food=food_instance)
            for image_instance in images_queryset:
                images.append(image_instance.image_url)
            food = {
                "name":food_instance.name,
                "price":food_instance.price,
                "images":images,
            }
            foods.append(food)

        reviews = []
        reviews_queryset = Review.objects.filter(restaurant=restaurant_instance)
        
        for r in reviews_queryset:
            print(r)
            review = {
                "user":{
                    "full_name":r.user.full_name,
                    "profile_image":r.user.profile_image,
                    # 리뷰 갯수
                    # ? 아무튼 갯수. 친구수인가 스토리 수인가. 
                },
                "content" : r.content,
                "rating":r.rating,
                "created_at":r.created_at,
            }
            print(review)

        restaurant = {
            "sub_category": restaurant_instance.sub_category.name,
            "name": restaurant_instance.name,
            "address": restaurant_instance.address,
            "phone_number": restaurant_instance.phone_number,
            "coordinate": restaurant_instance.coordinate,
            "open_time": restaurant_instance.open_time,
            "updated_at": restaurant_instance.updated_at,
            "foods":foods,
            "reviews":reviews,
        }

        print(restaurant)

        return JsonResponse({"message":"success", "result":restaurant}, status=200)


class ReviewView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            print(data)
            print(request.user)
            user_instance = request.user
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            print(restaurant_instance)
            content = data["content"]
            print(content)
            rating = data["rating"]
            print(rating)

            review = Review.objects.create(
                user=user_instance,
                restaurant=restaurant_instance,
                content = content,
                rating=rating
            )

            print(review)

            return JsonResponse({"message":"success"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
