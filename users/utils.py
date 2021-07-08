import jwt

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

import my_settings
from users.models import User

class ConfirmUser:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, request, *args, **kwargs):
        try:
            token   = request.headers.get("Authorization")
            decoded_token = jwt.decode(jwt=token, key=my_settings.SECRET_KEY,  algorithms=my_settings.ALGORITHM)

            if not decoded_token :
                raise ValidationError(message="NO_TOKEN")
            
            user_instance = User.objects.get(id=decoded_token["id"])
            request.user = user_instance
            
            return self.func(self, request, *args, **kwargs)
        
        except InvalidSignatureError:
            return JsonResponse({"message":"INVALID_SIGNATURE"}, status=400)
        
        except ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_SIGNATURE"}, status=400)
        
        except DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)
