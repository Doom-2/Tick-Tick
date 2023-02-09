import random
import string


def pwd_generator(length: int = 19) -> str:

    # define data
    lower: str = string.ascii_lowercase
    upper: str = string.ascii_uppercase
    num: str = string.digits

    # combine the data
    all_: str = lower + upper + num

    # use random
    temp: list = random.sample(all_, length)

    # create the password
    password = ''.join(temp)

    # print the password
    return password
