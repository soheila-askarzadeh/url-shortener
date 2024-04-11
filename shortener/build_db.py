"""create table"""
import sqlite3

def create_shortener_table():
    """create shortcode table"""
    conn = sqlite3.connect("shortener.db")
    columns = ["id_ INTEGER PRIMARY KEY", "shortcode  VARCHAR UNIQUE","url VARCHAR",
               "shortened_url VARCHAR UNIQUE", "created_date DATETIME","last_redirect DATETIME",
                "redirect_count INTEGER"]
    create_table_cmd = f"CREATE TABLE IF NOT EXISTS shortcode ({','.join(columns)})"
    conn.execute(create_table_cmd)
    conn.close()
