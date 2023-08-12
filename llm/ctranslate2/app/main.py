from fastapi import FastAPI, Request, Query
from fastapi import HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer
import ctranslate2


class FormChat(BaseModel):
    text: str
    temperature: float = 0.9
    top_p: float = 0.95
    top_k: int = 50
    max_length: int = 500


app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained('mesolitica/llama-7b-hf-1024-ms-qlora')
model = ctranslate2.Generator('app/ctranslate2', device='cuda', device_index=0)


@app.get('/')
async def get():
    return 'hello'


@app.post('/chat')
async def chat(
    form: FormChat,
    request: Request = None,
):
    form = form.dict()
    prompt = f"#User: {form['text']}\n#Bot: "

    o = model.generate_batch(
        [tokenizer.tokenize(prompt)],
        max_length=form['max_length'],
        sampling_temperature=form['temperature'],
        sampling_topp=form['top_p'],
        sampling_topk=form['top_k'],
        asynchronous=True,
    )
    o = o[0].result()
    return {'result': tokenizer.decode(tokenizer.convert_tokens_to_ids(o.sequences[0]))}
