from fastapi import FastAPI
import pyodbc

app = FastAPI()

## create connection
conn = pyodbc.connect(r'Driver={SQL Server};Server=MOHAMED\SQLEXPRESS;Database=Quran;Trusted_Connection=yes;')



@app.get("/surah/{surah_id}")
def get_surah_by_id(surah_id: int):
    result = {
        "name": "",
        "type": "",
        "nyah": "",
        "revolution_order": "",
        "content": ""
        }
    get_surah_query = 'select surah_name, type, nyah, revolution_order, ayat_text from surah join ayat on surah.surah_id = ayat.fk_surah_id where surah.surah_id = ? order by ayat_id asc'
    
    cursor = conn.cursor()
    cursor.execute(get_surah_query, surah_id)
    records = cursor.fetchall()

    for row in records:
        if len(result["name"]) == 0:
            result["name"] = row[0]
            result["type"] = row[1]
            result["nyah"] = row[2]
            result["revolution_order"] = row[3]
        
        result["content"] = result["content"] + row[4]
    

    return result


@app.get("/surah/{name}")
def get_surah_by_name(name: str):
    result = {
        "name": "",
        "type": "",
        "nyah": "",
        "revolution_order": "",
        "content": ""
        }
    get_surah_query = "select surah_name, type, nyah, revolution_order, ayat_text from surah join ayat on surah.surah_id where surah.surah_name = ? order by ayat_id asc"
    
    cursor = conn.cursor()
    cursor.execute(get_surah_query, name)
    records = cursor.fetchall()
    
    for row in records:
        if len(result["name"]) == 0:
            result["name"] = row[0]
            result["type"] = row[1]
            result["nyah"] = row[2]
            result["revolution_order"] = row[3]

        result["content"] = result["content"] + row[4]
    
    return result


@app.get("/ayat/{surah_number}/{ayat_number}")
def get_ayat_by_surah_number(surah_number: int, ayat_number: int):
    result = {
        "surah_number": surah_number,
        "ayat_number": ayat_number,
        "content": ""
    }
    get_ayat_query = 'select ayat_text from ayat where fk_surah_number = ? and ayat_id = ?'

    cursor = conn.cursor()
    cursor.execute(get_ayat_query, surah_number, ayat_number)
    result["content"] = cursor.fetchone()[0]

    return result


@app.get("/ayat/{surah_name}/{ayat_number}")
def get_ayat_by_surah_name(surah_name: int, ayat_number: int):
    result = {
        "surah_name": surah_name,
        "ayat_number": ayat_number,
        "content": ""
    }
    get_ayat_query = 'select ayat_text from ayat join surah where ayat.fk_surah_id = surah.surah_id where surah_name = ?, and ayat_id = ?'

    cursor =  conn.cursor()
    cursor.execute(get_ayat_query, surah_name, ayat_number)

    result["content"] = cursor.fetchone()[0]

    return result

