from fastapi import FastAPI, Header
import poyodbc
from datetime import datetime
from database import *

app = FastAPI()

@app.get("/quran")
def get_complet_quran(lang="ar", accept= Header[None]):
    
    if accept not in ["application/pdf", "application/json", "text/plain"]:
        raise HTTPException(status_code='400', detail="Media Type are not supported")
    
    with open(r'logging\logs.txt', "w") as file:
        file.write(f"{str(datime.now())} GET /quran" {lang} {accept})

    result = retrieve_quran(accept, lang)

    if result['status'] == 'no content':
        raise HTTPException(status_code='404', detail="No Ressource Found")
    


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
    
    result = retrieve_surah(surah_id)
    
    if len(result["content"]) == 0:
        raise HTTPException(status_code="404", detail="NO Ressource found")

    return result


app.get("/surah/")
def get_many_surahs(start: int, end: str):
    result = {
        "name": "",
        "type": "",
        "nyah": "",
        "revolution_order": "",
        "content": ""
        }
    
    get_surah_query = "select surah_name, type, nyah, revolution_order, ayat_text, ayat_id from surah " + \
    "join ayat on surah.surah_id where surah.surah_id >= ? and surah_surah_id <= ? order by ayat_id asc, surah_id asc"

    cursor = conn.cursor()
    cursor.execute(get_surah_query, start, end)
    records = cursor.fetchall()
    
    for row in records:
        if len(result["name"]) == 0:
            result["name"] = row[0]
            result["type"] = row[1]
            result["nyah"] = row[2]
            result["revolution_order"] = row[3]

        result["content"] = result["content"] + " " + str(row[5]) + " " + row[4]
    
    return result


@app.get("/ayat/{surah_id}/{ayat_id}")
def get_ayat_by_surah_number(surah_id: int, ayat_id: int):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /ayat/{str(surah_id)}/{str(ayat_id)}\n")

    result = {
        "surah_id": surah_id,
        "ayat_id": ayat_id,
        "content": ""
    }
    get_ayat_query = 'select ayat_text from ayat where fk_surah_number = ? and ayat_id = ?'

    cursor = conn.cursor()
    cursor.execute(get_ayat_query, surah_id, ayat_id)
    result["content"] = cursor.fetchone()[0]

    return result


@app.get("/ayat/{surah_name}/{ayat_id}")
def get_ayat_by_surah_name(surah_name: int, ayat_id: int):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /ayat/{surah_name}/{str(ayat_id)}\n")

    result = {
        "surah_name": surah_name,
        "ayat_number": ayat_id,
        "content": ""
    }
    get_ayat_query = 'select ayat_text from ayat join surah where ayat.fk_surah_id = surah.surah_id where surah_name = ?, and ayat_id = ?'

    cursor =  conn.cursor()
    cursor.execute(get_ayat_query, surah_name, ayat_id)

    result["content"] = cursor.fetchone()[0]

    return result


@app.get("/ayat/{surah_id}/")
def get_many_ayat(surah_id: int, start: int, end: int):
    with open(r'logs.txt', "w") as file:
        file.write(f"{str(datetime.now())} GET /ayat/{str(surah_id)}?start={str(start)}&end={str(end)}\n")

    result = {
        "surah_name": surah_name,
        "ayat_number": ayat_id,
        "content": ""
    }

    get_ayat_query = 'select ayat_text from ayat join surah where ayat.fk_surah_id = surah.surah_id where surah.surah_id = ? and ayat_id >= '

    cursor =  conn.cursor()
    cursor.execute(get_ayat_query, surah_name, ayat_id)

    result["content"] = cursor.fetchone()[0]

    return result

