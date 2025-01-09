import requests
import xml.etree.ElementTree as ET
import sqlite3
from datetime import datetime

decoded_api_key = "ArHxw5hx9EILGXFK1vw2+dunRCKjbV4ujb9ElJ2P4JlczkCT5lLgAtHa6HBFfjFYuFeNwunPQZ7dmZGK+bxu3g=="

def fetch_and_store_data(lawd_cd, deal_ymd):
    endpoint = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
    params = {
        'serviceKey': decoded_api_key,
        'LAWD_CD': lawd_cd,
        'DEAL_YMD': deal_ymd,
        'numOfRows': '1000',
        'pageNo': '1',
        'dataType': 'XML'
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        print(f"API 응답 내용 ({lawd_cd}):\n{response.text}")
        root = ET.fromstring(response.text)

        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d')

        for item in root.findall('.//item'):
            aptDong = item.find('aptDong').text if item.find('aptDong') is not None else None
            aptNm = item.find('aptNm').text if item.find('aptNm') is not None else None
            buildYear = int(item.find('buildYear').text) if item.find('buildYear') is not None and item.find('buildYear').text.isdigit() else None
            dealAmount = item.find('dealAmount').text.replace(',', '').strip() if item.find('dealAmount') is not None else None
            dealDay = int(item.find('dealDay').text) if item.find('dealDay') is not None and item.find('dealDay').text.isdigit() else None
            dealMonth = int(item.find('dealMonth').text) if item.find('dealMonth') is not None and item.find('dealMonth').text.isdigit() else None
            dealYear = int(item.find('dealYear').text) if item.find('dealYear') is not None and item.find('dealYear').text.isdigit() else None
            excluUseAr = float(item.find('excluUseAr').text) if item.find('excluUseAr') is not None else None
            floor = int(item.find('floor').text) if item.find('floor') is not None and item.find('floor').text.isdigit() else None
            sggCd = item.find('sggCd').text if item.find('sggCd') is not None else None
            umdNm = item.find('umdNm').text if item.find('umdNm') is not None else None

            try:
                cursor.execute('''
                    INSERT INTO real_estate (aptDong, aptNm, buildYear, dealAmount, dealDay, dealMonth, dealYear, excluUseAr, floor, sggCd, umdNm, reg_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (aptDong, aptNm, buildYear, dealAmount, dealDay, dealMonth, dealYear, excluUseAr, floor, sggCd, umdNm, now))
            except Exception as e:
                print(f"데이터 삽입 오류: {e}, 데이터: {ET.tostring(item, encoding='unicode')}")

        conn.commit()
        conn.close()
        print(f"{lawd_cd} 코드, {deal_ymd} 데이터 저장 완료.")

    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류 발생: {e}")
    except ET.ParseError as e:
        print(f"XML 파싱 오류 발생: {e}")

if __name__ == "__main__":
    # 서울시 전체 구 코드
    gu_list = [
        '11110', '11140', '11170', '11200', '11215', '11230', '11260', '11290', '11305',
        '11320', '11350', '11380', '11410', '11440', '11470', '11500', '11530', '11545',
        '11560', '11590', '11620', '11650', '11680', '11710', '11740'
    ]
    # 2024년 1월 데이터 가져오기
    deal_ymd = '202401'
    for gu_code in gu_list:
        fetch_and_store_data(gu_code, deal_ymd)