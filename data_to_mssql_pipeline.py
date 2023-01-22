
import json
import re
from connection import conn

def import_surats():
    ayats = clean_ayat_data()

    file = open(r"data\suras.json", "r", encoding="utf8")

    surah_json = dict(json.load(file))

    file.close()

    for surah_number in surah_json.keys():
        surah_meta_data = surah_json[surah_number]
        name = surah_meta_data["name"]
        type = surah_meta_data["type"]
        nayah = surah_meta_data["nAyah"]
        revelotion_order = surah_meta_data["revelationOrder"]
        
        # import surah_meta_data to database
        add_surah_query = "insert into surah(surah_id, surah_name, type, nyah, revolution_order) values(?,?,?,?,?)"
        cursor.execute(add_surah_query, surah_number, name, type, nayah, revelotion_order)
        print(f"surah number {surah_number} has been imported !")

        _start = int(surah_meta_data["start"])
        _end = int(surah_meta_data["end"])

        for i in range(_start, _end + 1):
            aya = ayats[i]
            foreign_key = surah_number
            #import aya to database
            add_ayat_query = "insert into ayat(ayat_id, ayat_text, fk_surah_id) values(?, ?, ?)"
            cursor.execute(add_ayat_query, i, aya, foreign_key)


def clean_ayat_data():
    ready_ayats = {}

    file = open(r"data\ayats.txt", "r", encoding="utf8")
    data = file.read()
    file.close()

    # remove license declaration
    ayats = re.split("-->", data)[1]

    # create a dictionary of index and ayat
    ayats = ayats.split('\n\n')[1:]

    for i in range(0, len(ayats) - 1, 2):
        index = ayats[i][2:]
        aya = ayats[i + 1]
        ready_ayats[int(index)] = aya

    return ready_ayats


if __name__ == "__main__":
    conn = conn()
    
    # sql cursor
    cursor = conn.cursor()

    import_surats()
    
    # commit the changes into database
    cursor.commit()
    cursor.close()
