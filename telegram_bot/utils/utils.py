from abc import ABC
import uuid
import string
import random

class Default(ABC):

    default_callback: str = f"default_callback"
    none_callback: str = f"none_callback"

# def slice_dict(start, end, dictionary: dict = {}):
#     for i, v in enumerate(my_dict.keys(), start=0):
#         print(i + 1, v)
#     return sliced_dict

# Пример словаря

# for i, v in enumerate(my_dict.keys(), start=0):
#     print(i+1, v)

# Выделение части словаря от ключа "a" до ключа "b"
# sliced_dict = slice_dict(my_dict, "a", "c")
# print(sliced_dict)

# import uuid
# import string
# import random
# import time
#
# n = 100
#
# start_time = time.time()
#
# my_dict = {"".join(random.sample(string.ascii_letters, 6)): {"id": str(uuid.uuid4())} for _ in range(0, n)}
# rand_index = random.randint(0, n)
# for i, v in enumerate(my_dict.values()):
#     if i == rand_index:
#         print(i, v)
#         break
#
# end_time = time.time()
# execution_time = end_time - start_time
#
# print(f"Время выполнения: {execution_time} секунд")
#
# from database3.telegram_bot.classes.api_requests import AdminAPI
# import asyncio
#
# dct: dict = asyncio.run(AdminAPI.get_user_classes(telegram_id=5)).get("data")
# my_dct: dict = {i: {v.get("name"): v.get("id")} for i, v in enumerate(dct.values(), start=1)}
# print(my_dct)
#
# for i, v in my_dct.items():
#     print([i for i in v.keys()][0])
#     print(list(v.keys())[0])
#
# print(list(my_dct[1].values())[0])


