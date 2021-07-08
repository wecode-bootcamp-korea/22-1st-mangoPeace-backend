import json
import bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.db.utils        import IntegrityError

from json.decoder           import JSONDecodeError

from users.models           import User
from users.validation       import validate_email, validate_full_name, validate_password, validate_phone_number

class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            full_name    = data["full_name"]
            email        = data["email"]
            password     = data["password"]
            phone_number = data["phone_number"]

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
                full_name    = full_name,
                email        = email,
                password     = hashed_password.decode(),
                phone_number = phone_number,
                )

            return JsonResponse({"message":"success"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message":"VALIDATION_ERROR"}, status=401)        

        except IntegrityError:
            return JsonResponse({"message":"INTEGRITY_ERROR"}, status=400)

        except Exception:
            return JsonResponse({"message":"UNCAUGHT_ERROR"}, status=400)
