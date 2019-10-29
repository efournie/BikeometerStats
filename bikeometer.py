import sqlite3
import matplotlib.pyplot as plt

def print_all_tables(conn):
    cur = conn.cursor()
    cur.execute('SELECT name from sqlite_master where type= "table"')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
def get_columns_names(conn, table_name='track_details_table'):
    cur = conn.cursor()
    cur.execute(f'SELECT name from PRAGMA_TABLE_INFO("{table_name}")')
    rows = cur.fetchall()
    return rows
    
def get_tracks_details(conn):
    cur = conn.cursor()
    cur.execute('SELECT * from track_details_table')
    rows = cur.fetchall()
    return rows
    
db_file = 'tracks.bk'
conn = conn = sqlite3.connect(db_file)
print('Table contents:')
print_all_tables(conn)
print('Tracks details:')
col_names = get_columns_names(conn)
tracks = get_tracks_details(conn)
print(col_names)
for track in tracks:
    print(track)