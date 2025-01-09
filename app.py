from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 전체 구 코드 매핑 (fetch_data.py에서 사용하는 목록과 동일)
district_mapping = {
    '11110': '종로구',
    '11140': '중구',
    '11170': '용산구',
    '11200': '성동구',
    '11215': '광진구',
    '11230': '동대문구',
    '11260': '중랑구',
    '11290': '성북구',
    '11305': '강북구',
    '11320': '도봉구',
    '11350': '노원구',
    '11380': '은평구',
    '11410': '서대문구',
    '11440': '마포구',
    '11470': '양천구',
    '11500': '강서구',
    '11530': '구로구',
    '11545': '금천구',
    '11560': '영등포구',
    '11590': '동작구',
    '11620': '관악구',
    '11650': '서초구',
    '11680': '강남구',
    '11710': '송파구',
    '11740': '강동구'
}

def get_latest_data_grouped_by_district():
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM real_estate WHERE reg_date = ?
    ''', (today,))
    data = cursor.fetchall()
    conn.close()

    # 구별로 데이터 그룹화
    grouped_data = {}
    for row in data:
        sgg_cd = row[9]  # sggCd (구 코드)
        if sgg_cd not in grouped_data:
            grouped_data[sgg_cd] = []
        grouped_data[sgg_cd].append(row)
    return grouped_data

@app.route('/')
def index():
    grouped_data = get_latest_data_grouped_by_district()
    return render_template('index.html', grouped_data=grouped_data, district_mapping=district_mapping)

if __name__ == '__main__':
    app.run(debug=True)