# Tutorial

## Static Files

- 使用StaticFiles从一个目录中自动服务静态文件
- pip install aiofiles
- from fastapi.staticfiles import StaticFiles
  app = FastAPI()
  app.mount("/static", StaticFiles(directory="static"), name="static")
- Mounting指的是在一个指定的路径上("/static")添加一个“独立”的应用application(StaticFiles(directory="static"))，然后这个应用（StaticFiles）处理这个子路径下的所有请求
- 这与使用APIRouter不同，因为一个mounted的应用程序是完全独立的，你的主应用中的OpenAPI和docs不会包含mounted的applicaiton的任何东西
- "/static"引用子应用将被挂在的子路径，这样任何从/static开始的路径都被子应用处理
- StaticFiles创建子应用，参数directory="static"指定这个文件服务应用服务的文件目录
- name="static"给这个子应用一个名字，它被FastAPI内部使用
