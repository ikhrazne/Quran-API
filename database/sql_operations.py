from connection import conn
import pandas as pd

conn = conn()


def retrieve_quran(media_type, lang):
    result = None
    
    if media_type == 'application/pdf':
        result = get_quran_as_pdf(lang=lang)
    else:
        result = get_plain_text_quran()
        
    return result


def get_quran_as_pdf(lang):
    cursor = conn.cursor()

    cursor.execute("select pdf_file from files where lang = ?", lang)
    record = cursor.fetchone()
    if record is None:
        return {"status": "no content", "content": ""}
    else:
        return {"status": "Ok", "content": record[0]}


def get_plain_text_quran(lang="ar"):
    result = {
        "status": "",
        "content": ""
    }
     
    quran_df = pd.read_sql(
        "select surah_id, surah_name, ayat_text from surah join ayat on surah.surah_id = ayat.fk_surah_id order by surah_id asc, ayat_id asc", conn
    )

    if quran_df.empty:
        result["status"] = "no content"
        return result
    
    quran_df["ayat_text"] = quran_df.groupby(["surah_id, surah_name"]).transform(quran_df["surah_name"] + " ".join(quran_df["ayat_text"]))
    
    result["status"] = "OK"
    result["content"] = quran_df.drop_duplicates()["ayat_text"]

    return result


def retrieve_surah(surah_iden) -> dict:
    result = {
        "name": "",
        "type": "",
        "nyah": "",
        "revolution_order": "",
        "content": ""
        }
    
    if type(surah_iden) == 'int':
        surah_df = pd.read_sql(
            'select surah_name, type, nyah, revolution_order, ayat_text, ayat_id from surah join ayat on surah.surah_id = ayat.fk_surah_id where surah.surah_id = ? order by ayat_id asc', 
            conn, params=[surah_iden]
            )
    else:
        surah_df = pd.read_sql(
            'select surah_name, type, nyah, revolution_order, ayat_text, ayat_id from surah join ayat on surah.surah_id = ayat.fk_surah_id where surah.surah_name = ? order by ayat_id asc', 
            conn, params=[surah_iden]
            )

    for index, row in surah_df.iterrows():
        if len(result["name"]) == 0:
            result["name"] = row[0]
            result["type"] = row[1]
            result["nyah"] = row[2]
            result["revolution_order"] = row[3]
        
        result["content"] = result["content"] + " " + str(index) + " " + row['ayat_text']
    
    return result


def retrieve_interval_in_surah(start: int, end: int):
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

def retrieve_ayat_by_surah_name(surah_id: int, ayat_id: int):
    result = {
        "surah_id": surah_id,
        "ayat_id": ayat_id,
        "content": ""
    }
    get_ayat_query = 'select ayat_text over(partition by fk_surah_number) from ayat where fk_surah_number = ?'

    df = pd.read_csv(get_ayat_query, conn, params=[ayat_id])
    
    if df.empty:
        return result
    
    result["content"] = df.iloc[ayat_id]

    return result


if __name__ == '__main__':
    pass