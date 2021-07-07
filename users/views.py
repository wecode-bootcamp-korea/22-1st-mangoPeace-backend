import json
import bcrypt
import jwt
import datetime

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from json.decoder import JSONDecodeError

from users.models import User
from users.validation import validate_email, validate_full_name, validate_password, validate_phone_number
import my_settings

# bcrypt 시켜서 저장
# ? : jwt토큰화를 회원가입에서 시켜야 하나
# ? : profile_url에서 한 것 처럼 조건부 할당은 어떤가? None을 nullable field에 넣으면 결과는 같은것 같다. 
# ? : regex validate에 대해 나름의 custom error를 만들고 싶다.
# ? :  datetime과 exp. 이게 확실한건가.
# ? : user구별. UserView에서 user을 구분할떄 토큰으로만 할까? 아니면 따로 body에 데이터를 받을까.

# userview에서 wishlist담아서 줘야함.

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            full_name = data["full_name"]
            email = data["email"]
            password = data["password"]
            phone_number = data["phone_number"]
            profile_url = data["profile_url"] if data.get("profile_url") else None

            if not validate_full_name(full_name):
                raise ValidationError(message=None)

            if not validate_email(email):
                raise ValidationError(message=None)

            if not validate_password(password):
                raise ValidationError(message=None)

            if not validate_phone_number(phone_number):
                raise ValidationError(message=None)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            User.objects.create(
                full_name=full_name,
                email=email,
                password=hashed_password.decode(),
                phone_number=phone_number,
                profile_url=profile_url
                )

            return JsonResponse({"message":"success"}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)        

        except ValidationError:
            return JsonResponse({"message":"VALIDATION_ERROR"}, status=400)        

        except IntegrityError:
            return JsonResponse({"message":"INTEGRITY_ERROR"}, status=400)        

        except Exception as error:
            print(error)
            print(error.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]

            if not validate_email(email):
                raise ValidationError(message=None)

            if not validate_password(password):
                raise ValidationError(message=None)

            user = User.objects.get(email=email)
            is_password_match = bcrypt.checkpw(password.encode(), user.password.encode())
            
            if not is_password_match:
                raise ValidationError(message=None)

            current_time = datetime.datetime.now()
            five_hours = datetime.timedelta(hours=5)
            exp = current_time + five_hours
            access_token = jwt.encode(
                {"id" : user.id, "exp":exp},
                my_settings.SECRET_KEY,
                my_settings.ALGORITHM
            )

            return JsonResponse({"message":"success", "access_token":access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)        

        except ValidationError:
            return JsonResponse({"message":"VALIDATION_ERROR"}, status=400)        

        except Exception as error:
            print(error)
            print(error.__class__)
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)

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
            "full_name":user_instance.full_name,
            "email":user_instance.email,
            "profile_url":user_instance.profile_url,
        }
        print(user)
        
        return JsonResponse({"message":"success","result":user}, status=200)
