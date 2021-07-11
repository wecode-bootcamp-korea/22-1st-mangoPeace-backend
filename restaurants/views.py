from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.db.models import Avg

from restaurants.models import SubCategory

class RestaurantListView(View):
    def get(self, request, sub_category_id):
        try:
            sub_categorys = SubCategory.objects.all()           
            sub_category_list = []
            for sub_category in sub_categorys:
                restaurants = sub_category.restaurants.all()                
                restaurant_list = []            
                for restaurant in restaurants:
                    restaurant_list.append({
                            "name"          : restaurant.name,
                            "address"       : restaurant.address,
                            "content"       : restaurant.review_set.order_by('?')[0].content,
                            "profile_url"   : restaurant.review_set.order_by('?')[0].user.profile_url,
                            "nickname"      : restaurant.review_set.order_by('?')[0].user.nickname,
                            "image"         : restaurant.foods.all()[0].images.all()[0].image_url,
                            "rating"        : round(restaurant.review_set.all().aggregate(Avg('rating'))['rating__avg'], 1)
                        })
                restaurant_list = sorted(restaurant_list, key=lambda x:x['rating'], reverse=True)
                    
                return JsonResponse({"message":"success", "result":restaurant_list}, status=200)
            
        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)