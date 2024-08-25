from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "Helsinki-NLP/opus-mt-en-ru"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

tokenizer.save_pretrained(Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')
model.save_pretrained(Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')
