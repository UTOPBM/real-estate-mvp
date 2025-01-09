import sqlite3

def create_table():
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_estate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aptDong TEXT,
            aptNm TEXT,
            buildYear INTEGER,
            dealAmount TEXT,
            dealDay INTEGER,
            dealMonth INTEGER,
            dealYear INTEGER,
            excluUseAr REAL,
            floor INTEGER,
            sggCd TEXT,
            umdNm TEXT,
            reg_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("데이터베이스 테이블 생성 완료.")