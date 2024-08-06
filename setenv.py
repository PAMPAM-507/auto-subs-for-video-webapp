#!/bin/sh

# from dotenv import load_dotenv
# import os

# load_dotenv()

# my_variable = os.getenv("EMAIL_HOST_USER")
# print(my_variable)  # Должно вывести "my_value"

import os
os.system(
        f'cd ./ && whisper test3.mp4 --model tiny --language en'
    )

