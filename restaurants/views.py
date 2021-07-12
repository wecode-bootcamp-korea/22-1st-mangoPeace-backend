from django.http        import JsonResponse
from django.views       import View

from restaurants.models import Image, Restaurant

class RestaurantFoodImageView(View):
    def get(self, request, restaurant_id):
        try:
            foods  = Restaurant.objects.get(id=restaurant_id).foods.all()
            images = []

            for f in foods:
                images = Image.objects.filter(food=f)
                
                for i in images:
                    images.append(i.image_url)
            
            return JsonResponse({"message":"success", "result":images}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)