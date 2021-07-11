import json
import bcrypt
import jwt
import datetime

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.db.utils        import IntegrityError

from json.decoder           import JSONDecodeError

import my_settings

from users.models           import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.validate(data):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=401)        

            nickname     = data["nickname"]
            email        = data["email"]
            password     = data["password"]
            phone_number = data["phone_number"]

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message":"INTEGRITY_ERROR"}, status=400)

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

        else:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            User.objects.create(
            nickname     = nickname,
            email        = email,
            password     = hashed_password.decode(),
            phone_number = phone_number,
            )

            return JsonResponse({"message":"success"}, status=201)

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            user     = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=400)        

        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)        

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)        

        except Exception as e:
            print(e)
            print(e.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
        
        else:
            exp           = datetime.datetime.now() + datetime.timedelta(hours=24)
            access_token  = jwt.encode(
                payload   = {"id" : user.id, "exp" : exp},
                key       = my_settings.SECRET_KEY,
                algorithm = my_settings.ALGORITHM
            )

            return JsonResponse({"message":"success", "access_token":access_token}, status=200)

class UserView(View):
    def get(self, request):
        access_token = request.headers["Authorization"]
        user_id = jwt.decode(
            jwt=access_token,
            key=my_settings.SECRET_KEY,
            algorithms=my_settings.ALGORITHM
            )["id"]
        user_instance = User.objects.get(id=user_id)
        wish_list = []
        wish_list_queryset = user_instance.wishlist_restaurants.all()
        print(wish_list_queryset)
        for w in wish_list_queryset:
            print(w)
        user = {
            "nickname":user_instance.nickname,
            "email":user_instance.email,
            "profile_url":user_instance.profile_url,
        }
        print(user)
        
        return JsonResponse({"message":"success","result":user}, status=200)
