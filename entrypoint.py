from fastapi import FastAPI, Cookie
from typing import Optional
from pydantic import BaseModel
import copy

class DataBlob(BaseModel):
    identity: int
    shard: str | None = None

class Config(BaseModel):
    domani: int
    def counting_worms(self):
        print("numero di vermi "+ str(self.domani))

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello da fast API"}

#url parameters
@app.get("/pathway/{path_id}/")
#questo è pydantic
def handle_path(path_id: int):
    return {"path": path_id}

#queryparameters
@app.get("/queryp/")
def qp(needy: int,qp: str | None):
    needy = needy + 1
    return qp+str(needy)

# request body
@app.post("/shard/")
async def create_shard(dataBlob: DataBlob):
    obj = dataBlob
    return obj



# request body with queryparams and url params
@app.post("/shard/inferno/{shard_id}")
async def create_shard(dataBlob: DataBlob, shard_id: int, pelle: str | None):
    obj = {**dataBlob.dict()}
    obj.update({"nuevo_valor": shard_id})
    obj.update({"pelle": pelle})
    return obj

@app.post("/config/")
def a(config: Config):
    obj = config
    obj.counting_worms()
    return obj


# non va
@app.get("/cookie/")
def cookie(current_id: str = Cookie(default=None)):
    return current_id

# response model return type
"""
posso definire dei valori di ritorno dichiarati così da usare pydantic per fare la validazione dei dati anche sul ritorno della funzione.
Però c'è un però, io ritorno in realtà un dizionario mentre sul codice definisco un oggetto pydantic.

questo si risolve mettendo il decorator "response_model"= il mio modello di pydantic e come ritorno mettere -> any
"""

@app.get("/semplice/")
def return_semplice() -> DataBlob:
    b = DataBlob(identity=1,shard="123")
    return b

@app.get("/speciale/", response_model=DataBlob)
def return_speciale() -> any:
    return DataBlob(identity=2,shard="forse domani")

