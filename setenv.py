#!/bin/sh

# from dotenv import load_dotenv

# load_dotenv()

import os



my_variable = os.environ.get("SECRET_KEY_SUBS")
print(my_variable)  # Должно вывести "my_value"

# import os
# os.system(
#         f'cd ./ && whisper test3.mp4 --model tiny --language en'
#     )

