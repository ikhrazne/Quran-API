
import json
import re


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

        add_surah_query = "insert into surah(surah_id, name, type, nyah, revelotion_order) values(?,?,?,?,?)"

        _start = int(surah_meta_data["start"])
        _end = int(surah_meta_data["end"])

        for i in range(_start, _end):
            aya = ayats[i]
            foreign_key = surah_number
            add_ayat_query = "insert into ayat(ayat_id, aya, fk_surah_id) values(?, ?, ?)"


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
    import_surats()
