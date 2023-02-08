from connection import conn
import pandas as pd


def retrieve_quran(media_type, lang):
    result = None
    
    if media_type == 'application/pdf':
        pass
    elif media_type == 'text/plain':
        pass
    else:
        pass 
        
    return result


def get_plain_text_quran(lang="ar"):
    result = {
        "status": "",
        "content": ""
    }
     
    quran_df = pd.read_sql(
        "select surah_id, surah_name, ayat_text from surah join ayat on surah.surah_id = ayat.fk_surah_id order by ayat_id asc", conn
    )

    if df.empty:
        result["status"] = "no content"
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
            params=[surah_iden],conn
            )
    else:
        surah_df = pd.read_sql(
            'select surah_name, type, nyah, revolution_order, ayat_text, ayat_id from surah join ayat on surah.surah_id = ayat.fk_surah_id where surah.surah_name = ? order by ayat_id asc', 
            params=[surah_iden], conn
            )

    for index, row in surah_df.iterrows():
        if len(result["name"]) == 0:
            resutl["name"] = row[0]
            result["type"] = row[1]
            result["nyah"] = row[2]
            result["revolution_order"] = row[3]
        
        result["content"] = result["content"] + " " + str(index) + " " + row['ayat_text']
    
    return result


def retrieve_ayat():
    pass


if __name__ == '__main__':
    pass