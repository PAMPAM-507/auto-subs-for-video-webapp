# from pathlib import Path
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model_name = "Helsinki-NLP/opus-mt-en-ru"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# tokenizer.save_pretrained(Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')
# model.save_pretrained(Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')

# import torch


# print(torch.cuda.is_available())
# if torch.cuda.is_available():
#     for i in range(torch.cuda.device_count()):
#         print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
# else:
#     print("CUDA is not available. No GPU found.")


# import redis


# with redis.Redis(host='localhost', port=6380, db=0) as r:
        
        
#     r.delete(f'moviepy_progress{10}')
#     r.delete(f'whisper_progress{10}')
    
    
    
#     print(list(r.scan_iter('*')))