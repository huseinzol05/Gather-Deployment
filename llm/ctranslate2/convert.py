import ctranslate2
import os

folder = 'app/ctranslate2'
if not os.path.exists(folder):
    converter = ctranslate2.converters.TransformersConverter('mesolitica/llama-7b-hf-1024-ms-qlora')
    converter.convert(folder, quantization='int8_bfloat16', force=True)