from fastapi import FastAPI

import models
from database import engine
from routers.admin.v1 import api as admin_v1

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin_v1.router)
