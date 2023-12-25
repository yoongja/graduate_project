import csv
import math
from datetime import datetime

import fitz
import pandas as pd


# 하버사인 함수 정의
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km * 1000

# PDF에서 시위 데이터 추출
path = f"./demo_{datetime.now().strftime('%Y%m%d')}.pdf"
doc = fitz.open(path)
data = []

# 역 정보 데이터 불러오기
station = pd.read_excel('all_train.xlsx')
select_station = station[['역번호', '역사명', '노선번호', '역위도', '역경도']]
station_data = select_station.set_index('역사명').to_dict(orient='index')

for page in doc:
    text = page.get_text()
    lines = text.split('\n')
    for line in lines:
        if ',' in line:
            components = line.split(',')
            if len(components) >= 4:
                place, time, lat, lon = components[0], components[1], float(components[2]), float(components[3])
                # 가장 가까운 역 찾기
                closest_station = None
                min_distance = float('inf')
                for station_name, station_info in station_data.items():
                    station_lat = station_info['역위도']
                    station_lon = station_info['역경도']
                    dist = haversine(lat, lon, station_lat, station_lon)
                    if dist < min_distance:
                        min_distance = dist
                        closest_station = station_name
                nearest_station = closest_station or '가까운 역 없음'
                data.append([place, time, nearest_station])

# CSV 파일로 저장
csv_path = f"./demo_{datetime.now().strftime('%Y%m%d')}.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['시위장소', '시위 시간', '근처역'])
    for row in data:
        writer.writerow(row)
