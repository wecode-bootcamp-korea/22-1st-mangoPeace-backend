from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.db.models import Avg

from restaurants.models import SubCategory

class MainListView(View):
    def get(self, request, category_id):
        try:
            subcategorys = SubCategory.objects.all()           
            subcategory_list = []
            for subcategory in subcategorys:                 
                subcategory_list.append({
                    "image" : subcategory.restaurants.all()[0].food_set.all()[0].image_set.all()[0].image_url                
                })

            return JsonResponse({"message":"success", "result":subcategory_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)