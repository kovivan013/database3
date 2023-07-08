import uuid
import random
import string

def gen_uuid():
    return uuid.uuid4()

def gen_invite_code():

    characters: str = string.ascii_letters + string.digits
    invite_code: str = ""
    for i in range(1,4):
        invite_code += "".join(random.choice(characters) for _ in range(3)) + "-" if i < 3 else "".join(random.choice(characters) for _ in range(3))
    return invite_code