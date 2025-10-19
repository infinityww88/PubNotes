# Overview

## Key feature

- Fast：very high performance，on par with Nodejs and Go(thanks to Starlette and Pydantic)
- Fast to Code：increase the speed to develop features by 200% to 300%
- Easy：easy to use and learn，less time reading docs
- Short：Minimize code duplication，more shorter，fewer human errors(bugs)
- Robust：production-ready，automatic interactive documentation
- Standard-based：Based on (full compatible with) the open standards for APIs: OpenAPI(Swagger) and JSON schema

## Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("items/{item_id}")
async def read_items(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}
```

```sh
uvicorn main:app --reload
```

main：main.py

app：main.py中创建的FastAPI变量

reload：当代码有修改时，server自动重启，通常用于development

自动生成的api文档

- 127.0.0.1:8000/doc
- 127.0.0.1:8000/redoc

## Put Example

```python
from pydantic import BaseModel

class Item(BaseModel):
  name: str
  price: float
  is_offer: bool = None

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
  return {"item_name": item.name, "item_id": item_id}
```
