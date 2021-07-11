import os
import sys
import csv
import django

os.chdir('.')
# 결국 os가 파악한 현재경로가 중요한거 아냐? os.path쓸 필요가 ?
BASE_DIR = os.getcwd()

# sys : 파이썬 라이브러리가 설치되어 있는 디렉터리를 확인할 수 있다.
sys.path.append(BASE_DIR)

# python실행할때 현재 프로젝트의 settings.py경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mangoPeace.settings")

# django shell 실행
django.setup()

from users.models import *
from restaurants.models import *

CSV_PATH = 'users/mango.csv'

with open(CSV_PATH, encoding="utf8", mode="r") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:

# 메뉴 만들기 (다음을 위해서. 3명의 변태들 .)

        # if not Menu.objects.filter(name=row["menu"]).exists():
        #     menu = Menu.objects.create(name=row["menu"])
        
# # 카테고리 만들기 (지독한 사람들)

        # if not Category.objects.filter(name=row["category"]).exists():
        #     menu = Menu.objects.get(name=row["menu"])
        #     Category.objects.create(name=row["category"], menu=menu)

# # 서브 카테고리 만들기

        # if not SubCategory.objects.filter(name=row["sub_category"]).exists():
        #     category         = Category.objects.get(name=row["category"])
        #     SubCategory.objects.create(name=row["sub_category"], category=category)
        
# # 레스토랑 만들기

        # sub_category   = SubCategory.objects.get(name=row["sub_category"])
        # if not Restaurant.objects.filter(name=row["restaurant_name"], phone_number=row["phone_number"]).exists():
        #     Restaurant.objects.create(name=row["restaurant_name"], sub_category=sub_category, address = row["address"], 
        #     phone_number = row["phone_number"], coordinate = row["coordinate"], open_time = row["open_time"])

# # 푸드 만들기 만들기

        restaurant = Restaurant.objects.get(name=row["restaurant_name"])
        food = Food.objects.create(name=row["food_name"], restaurant=restaurant, price=row["price"])

# 푸드 만들기 만들기
        Image.objects.create(image_url=row["image_url"], food = food)