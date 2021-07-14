from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from restaurants.models import Restaurant, Image

class FilteringVeiw(View):
    def get(self, request):
        keyword        = request.GET.getlist('keyword', None)
        
        q = Q()
        if keyword:
            q &= Q(name__in = keyword)

        category_restaurants        = Restaurant.objects.filter(sub_category__category__name__in=keyword)
        sub_category_restaurants    = Restaurant.objects.filter(sub_category__name__in=keyword)
        restaurants                 = Restaurant.objects.filter(q)
        category_food_images        = Image.objects.filter(food__restaurant__sub_category__category__name__in=keyword)
        sub_category_food_images    = Image.objects.filter(food__restaurant__sub_category__name__in=keyword)
        restaurant_food_images      = Image.objects.filter(food__restaurant__name__in=keyword)

        category_result = [{
            "restaurantID"          : category_restaurant.id,
            "restaurantName"        : category_restaurant.name,
            "restaurantAddress"     : category_restaurant.address,
            "restaurantPhoneNum"    : category_restaurant.phone_number,
            "restaurantCoordinate"  : category_restaurant.coordinate,
            "restaurantOpenTime"    : category_restaurant.open_time,
            "food_image_url"        : category_food_images.first().image_url if category_food_images.first() else "",
        }for category_restaurant in category_restaurants]

        sub_category_result=[{
            "restaurantID"          : sub_category_restaurant.id,
            "restaurantName"        : sub_category_restaurant.name,
            "restaurantAddress"     : sub_category_restaurant.address,
            "restaurantPhoneNum"    : sub_category_restaurant.phone_number,
            "restaurantCoordinate"  : sub_category_restaurant.coordinate,
            "restaurantOpenTime"    : sub_category_restaurant.open_time,
            "food_image_url"        : sub_category_food_images.first().image_url if category_food_images.first() else "",
        }for sub_category_restaurant in sub_category_restaurants]

        restaurant_result=[{
            "restaurantID"          : restaurant.id,
            "restaurantName"        : restaurant.name,
            "restaurantAddress"     : restaurant.address,
            "restaurantPhoneNum"    : restaurant.phone_number,
            "restaurantCoordinate"  : restaurant.coordinate,
            "restaurantOpenTime"    : restaurant.open_time,
            "food_image_url"        : restaurant_food_images.first().image_url if category_food_images.first() else "",
        }for restaurant in restaurants]

        return JsonResponse({
            "category_result":category_result,
            "sub_category_result":sub_category_result,
            "restaurant_result":restaurant_result
            }, status=200)