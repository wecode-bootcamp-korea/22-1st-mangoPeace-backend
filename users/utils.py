import jwt

from django.http.response import JsonResponse

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

import my_settings
from users.models import User

class ConfirmUser:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({"message" : "ACCESS_TOKEN_REQUIRED"})
            
            payload      = jwt.decode(jwt=access_token, key=my_settings.SECRET_KEY,  algorithms=my_settings.ALGORITHM)
            user         = User.objects.get(id=payload["id"])
            request.user = user
            
            return self.func(self, request, *args, **kwargs)
        
        except InvalidSignatureError:
            return JsonResponse({"message":"INVALID_SIGNATURE"}, status=400)
        
        except ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_SIGNATURE"}, status=400)
        
        except DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=404)