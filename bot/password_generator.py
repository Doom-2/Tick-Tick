import random
import string


def pwd_generator(length: int = 19) -> str:

    # define data
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    # symbols = string.punctuation

    # combine the data
    all_ = lower + upper + num

    # use random
    temp = random.sample(all_, length)

    # create the password
    password = ''.join(temp)

    # print the password
    return password
