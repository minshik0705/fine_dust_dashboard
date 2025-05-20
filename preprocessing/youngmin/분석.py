import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ——— 한글 폰트 설정 시작 ———
# Windows에서 맑은 고딕 사용
mpl.rcParams['font.family'] = 'Malgun Gothic'
# 음수 마이너스 기호가 깨지는 문제 방지
mpl.rcParams['axes.unicode_minus'] = False
# ——— 한글 폰트 설정 끝 ———

# 1. 데이터 로드 및 전처리
pollution = pd.read_csv(r'일별평균대기오염도_2020-utf8.csv', encoding='utf-8-sig')
disease   = pd.read_csv(
    r'C:\Users\Melo\Desktop\DE\team_project\2차\국내 주요 도시 미세먼지 및 호흡기-혈관 질환 발생 수 데이터'
    r'\전국7개도시_인구10만명당_주요질병진단수_201101_202006-utf8.csv',
    encoding='utf-8-sig', skiprows=3
)

# 날짜 컬럼 파싱
pollution['date'] = pd.to_datetime(pollution['측정일시'].astype(str), format='%Y%m%d')
disease  ['date'] = pd.to_datetime(disease['연월'].astype(str), format='%Y%m')

# 월별 평균으로 집계
pollutant_cols = [
    '이산화질소농도(ppm)', '오존농도(ppm)', '일산화탄소농도(ppm)',
    '아황산가스농도(ppm)', '미세먼지농도(㎍/㎥)', '초미세먼지농도(㎍/㎥)'
]
daily_poll = pollution.groupby('date')[pollutant_cols].mean()
monthly_poll = daily_poll.resample('M').mean().reset_index()

disease_cols = [
    '폐암(C34)', '만성폐쇄성폐질환(J44)',
    '하기도감염(J20-22)', '허혈성심질환(I20-22)', '뇌졸중(I60-64)'
]
monthly_dis = (
    disease
    .groupby('date')[disease_cols]
    .mean()
    .resample('M')
    .mean()
    .reset_index()
)

# 2020년 데이터만 필터링
monthly_dis = monthly_dis[monthly_dis['date'].dt.year == 2020]
monthly_poll = monthly_poll[monthly_poll['date'].dt.year == 2020]

# 2. 병합
df = pd.merge(monthly_dis, monthly_poll, on='date', how='inner')

# 3. 상관계수 행렬 계산
corr = df[pollutant_cols + disease_cols].corr().loc[pollutant_cols, disease_cols]
print("■ 미세먼지 vs 질병 상관계수 행렬 ■")
print(corr)

# 4. 히트맵 그리기
plt.figure()
plt.imshow(corr.values, aspect='auto')
plt.colorbar(label='Pearson r')
plt.xticks(range(len(disease_cols)), disease_cols, rotation=45, ha='right')
plt.yticks(range(len(pollutant_cols)), pollutant_cols)
plt.title('미세먼지-질병 상관계수 Heatmap')
plt.tight_layout()
plt.show()

# 5. 상관도가 큰 상위 4개 페어 산점도
pairs = corr.abs().stack().sort_values(ascending=False)
top4 = pairs.head(4).index.tolist()
for pollutant, disease_name in top4:
    plt.figure()
    plt.scatter(df[pollutant], df[disease_name])
    plt.xlabel(pollutant)
    plt.ylabel(disease_name)
    plt.title(f'{disease_name} vs {pollutant} (r = {corr.loc[pollutant, disease_name]:.2f})')
    plt.tight_layout()
    plt.show()
