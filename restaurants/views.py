from django.http        import JsonResponse
from django.views       import View
from restaurants.models import Image, Restaurant

class RestaurantFoodImageView(View):
    def get(self, request, restaurant_id):
        try:
            foods_queryset = Restaurant.objects.get(id=restaurant_id).foods.all()
            images         = []

            for food_instance in foods_queryset:
                images_queryset = Image.objects.filter(food=food_instance)
                
                for image_instance in images_queryset:
                    images.append(image_instance.image_url)
            
            return JsonResponse({"message":"success", "result":images}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=400)