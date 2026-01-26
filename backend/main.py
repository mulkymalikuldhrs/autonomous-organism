from fastapi import FastAPI
from .database import engine
from .sense_engine import models as sense_models
from .memory_engine import models as memory_models
from .api.main import app as api_app

sense_models.Base.metadata.create_all(bind=engine)
memory_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/api", api_app)

@app.get("/")
def read_root():
    return {"message": "ORGANISME SAAS OTONOM is running."}
