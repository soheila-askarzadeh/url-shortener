"""create table"""
import sqlite3

def create_shortener_table():
    """create shortcode table"""
    conn = sqlite3.connect("shortener.db")
    columns = ["id_ INTEGER PRIMARY KEY", "shortcode  VARCHAR UNIQUE","url VARCHAR UNIQUE",
               "shortened_url VARCHAR UNIQUE", "createDate DATETIME","lastRedirect DATETIME",
                "redirectCount INTEGER"]
    create_table_cmd = f"CREATE TABLE IF NOT EXISTS shortcode ({','.join(columns)})"
    conn.execute(create_table_cmd)
    conn.close()

create_shortener_table()
