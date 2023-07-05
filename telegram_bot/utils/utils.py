from abc import ABC

class Default(ABC):

    default_callback: str = f"default_callback"
    none_callback: str = f"none_callback"

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

