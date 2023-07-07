from abc import ABC

class Default(ABC):

    default_callback: str = f"default_callback"
    none_callback: str = f"none_callback"

import uuid

def valid_uuid(guid: str):
    try:
        uuid_obj = uuid.UUID(guid)
        return str(uuid_obj) == guid
    except ValueError:
        return False

# def slice_dict(start, end, dictionary: dict = {}):
#     for i, v in enumerate(my_dict.keys(), start=0):
#         print(i + 1, v)
#     return sliced_dict

# Пример словаря
my_dict: dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

my_list: list = [1,2,3]

# for i, v in enumerate(my_dict.keys(), start=0):
#     print(i+1, v)

def slice_dict(start, end, dictionary: dict = {}):
    for i in range(1, start+1):
        dictionary.pop(i)
    my_dict = {i: v for i, v in reversed(dictionary.items())}
    for i in range(len(dictionary), end):
        dictionary.pop(i)

print(my_dict)
my_dict = {i: v for i, v in reversed(my_dict.items())}
print(my_dict)

slice_dict(start=9, end=20, dictionary=my_dict)
print(my_dict)



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


