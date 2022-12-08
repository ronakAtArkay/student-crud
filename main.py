from fastapi import FastAPI
from routers.admin.v1 import api as admin_v1
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin_v1.router)