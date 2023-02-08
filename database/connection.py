 ## connection to sql server

import pyodbc

def conn():
    return pyodbc.connect(r'Driver={SQL Server};Server=MOHAMED\SQLEXPRESS;Database=Quran;Trusted_Connection=yes;')


if __name__ == '__main__':
    pass
