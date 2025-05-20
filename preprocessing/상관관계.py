import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# ——— 한글 폰트 설정 시작 ———
# Windows에서 맑은 고딕 사용
mpl.rcParams['font.family'] = 'Malgun Gothic'
# Linux/macOS에서 나눔고딕 직접 경로 지정 예시:
# font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
# mpl.font_manager.FontProperties(fname=font_path)
# mpl.rcParams['font.family'] = 'NanumGothic'

# 음수 마이너스 기호가 깨지는 문제 방지
mpl.rcParams['axes.unicode_minus'] = False
# 1) 데이터 로드
df = pd.read_csv(r'C:\Users\Melo\Desktop\DE\team_project\2차\국내 주요 도시 미세먼지 및 호흡기-혈관 질환 발생 수 데이터\pm10_disease_with_precipitation-utf8.csv', encoding='utf-8-sig')

# 컬럼명에 끼어있는 개행문자 제거
df.columns = df.columns.str.replace('\n', '', regex=False).str.strip()

# 2) 컬럼명 정의
# 2) 필요한 칼럼 및 집계
from matplotlib.lines import Line2D
# 2) 연월 → year, month 분리
df['연월'] = df['연월'].astype(str)
df['year']  = df['연월'].str[:4].astype(int)
df['month'] = df['연월'].str[4:6].astype(int)

# 3) 질병 합계 컬럼 생성
disease_cols = [
    '폐암(C34)', '만성폐쇄성폐질환(J44)',
    '하기도감염(J20-22)', '허혈성심질환(I20-22)', '뇌졸중(I60-64)'
]
df['disease_sum'] = df[disease_cols].sum(axis=1)

# 4) 주요 컬럼 정의
rain_col = '강수량'
pm10_col = 'PM10'

# 5) 연도별로 개별 플롯 생성 및 저장
for yr in sorted(df['year'].unique()):
    sub = df[df['year'] == yr].sort_values('month')
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    # 왼쪽 y축: 질병 환자 수 합계
    ax1.scatter(
        sub[rain_col], sub['disease_sum'],
        c=sub['month'], cmap='tab20', marker='o'
    )
    ax1.set_xlabel('강수량 (mm)')
    ax1.set_ylabel('질병 환자 수 합계\n(인구 10만명당)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, linestyle='--', alpha=0.4)

    # 오른쪽 y축: PM10 농도
    ax2 = ax1.twinx()
    ax2.scatter(
        sub[rain_col], sub[pm10_col],
        c=sub['month'], cmap='tab20', marker='s'
    )
    ax2.set_ylabel('PM10 농도 (㎍/㎥)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'{yr}년 – 강수량 vs 질병 환자 수 & PM10 농도')
    plt.tight_layout()
    
    # 파일로 저장 (주석 해제하여 사용)
    plt.savefig(f'rain_vs_disease_pm10_{yr}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)