from http.client import HTTPException
from fastapi import FastAPI, Header, File
from datetime import datetime
from database import *
from database.sql_operations import retrieve_ayat_by_surah_name, retrieve_interval_in_surah, retrieve_quran, retrieve_surah

app = FastAPI()

@app.get("/quran")
def get_complet_quran(lang="ar", accept= Header[None]):
    
    with open(r'logging\logs.txt', "w") as file:
         file.write(f"{str(datetime.now())} GET /quran {lang} {accept}\n")
    
    if accept not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code='400', detail="Media Type are not supported")

    result = retrieve_quran(accept, lang)

    if result['status'] == 'no content':
        raise HTTPException(status_code='404', detail="No Ressource Found")
    
    if type(result["content"]) == "bytes":
        return File(result["content"])
    
    return result


@app.get("/surah/{surah_id}")
def get_surah_by_id(surah_id: int):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /surah/{str(surah_id)}\n")
    
    result = retrieve_surah(surah_id)
    
    if len(result["content"]) == 0:
        raise HTTPException(status_code="404", detail="NO Ressource found")
    
    return result


@app.get("/surah/{name}")
def get_surah_by_name(name: str):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /surah/{name}\n")
    
    result = retrieve_surah(name)
    
    if len(result["content"]) == 0:
        raise HTTPException(status_code="404", detail="NO Ressource found")

    return result


app.get("/surah/")
def get_many_surahs(start: int, end: str):
    result = retrieve_interval_in_surah(start, end)
    
    if result["content"] == "":
        raise HTTPException(status_code="404", detail="No Ressource Found")
    
    return result


@app.get("/ayat/{surah_id}/{ayat_id}")
def get_ayat_by_surah_number(surah_id: int, ayat_id: int):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /ayat/{str(surah_id)}/{str(ayat_id)}\n")

    result = retrieve_ayat_by_surah_name(surah_id, ayat_id)
    
    if result["content"] == "":
        raise HTTPException(status_code="404", detail="No Ressource Found")

    return result

