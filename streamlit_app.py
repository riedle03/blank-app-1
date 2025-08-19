import streamlit as st
import pandas as pd
from scipy.stats import ttest_rel
import plotly.graph_objects as go
import plotly.express as px

# --- 1. 앱 기본 설정 ---
st.set_page_config(layout="wide", page_title="대응표본 t-검정 분석기")

st.title("📄 논문용 사전-사후 데이터 분석")
st.subheader("대응표본 t-검정(Paired Samples t-test) 및 시각화")
st.write("---")

# --- 2. 파일 업로드 기능 ---
# 사이드바에 파일 업로더 배치
with st.sidebar:
    st.header("1. 데이터 업로드")
    uploaded_file = st.file_uploader("분석할 CSV 파일을 업로드하세요.", type=['csv'])

# 파일이 업로드되었을 때만 나머지 UI 표시
if uploaded_file is not None:
    # 한글 깨짐 방지를 위한 인코딩 설정
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        st.error("파일 인코딩 오류입니다. 'UTF-8' 또는 'CP949'로 저장된 CSV 파일을 업로드해주세요.")
        st.stop()
        
    st.header("📋 업로드된 데이터 미리보기")
    st.dataframe(df.head())
    
    # 데이터프레임의 컬럼 목록 가져오기
    options = df.columns.tolist()

    # --- 3. 사전-사후 변수 선택 기능 ---
    st.header("🔍 변수 선택")
    
    col1, col2 = st.columns(2)
    with col1:
        # 사전 검사 변수 선택 (다중 선택)
        pre_vars = st.multiselect(
            '사전 검사 변수 선택 (Pre-test)',
            options,
            help="분석할 사전 검사 변수를 순서대로 선택하세요."
        )
    with col2:
        # 사후 검사 변수 선택 (다중 선택)
        post_vars = st.multiselect(
            '사후 검사 변수 선택 (Post-test)',
            options,
            help="사전 검사와 짝을 이룰 사후 검사 변수를 순서대로 선택하세요."
        )
        
    # 선택된 변수 쌍의 개수가 일치하는지 확인
    if pre_vars and post_vars and len(pre_vars) != len(post_vars):
        st.warning("⚠️ 사전 검사와 사후 검사 변수의 개수가 일치해야 합니다. 순서에 맞게 다시 선택해주세요.")
    
    # --- 4. 데이터 분석 실행 ---
    st.write("---")
    if st.button('🚀 분석 실행', type="primary"):
        # 변수가 선택되었고, 쌍의 개수가 맞는지 최종 확인
        if not pre_vars or not post_vars or len(pre_vars) != len(post_vars):
            st.error("분석을 실행하려면 사전-사후 변수 쌍을 올바르게 선택해주세요.")
        else:
            # 분석 결과를 저장할 리스트 초기화
            results = []

            # 선택된 각 변수 쌍에 대해 반복적으로 분석 수행
            for pre_var, post_var in zip(pre_vars, post_vars):
                
                # 결측치(NaN)가 있는 행을 제거하여 쌍을 맞춤
                temp_df = df[[pre_var, post_var]].dropna()
                
                # 데이터가 충분한지 확인
                if len(temp_df) < 2:
                    st.warning(f"'{pre_var}'와 '{post_var}' 쌍은 유효한 데이터가 부족하여 분석에서 제외됩니다.")
                    continue
                
                pre_data = temp_df[pre_var]
                post_data = temp_df[post_var]

                # 대응표본 t-검정 실행
                t_stat, p_value = ttest_rel(pre_data, post_data)
                
                # 결과 저장
                results.append({
                    '사전 변수': pre_var,
                    '사후 변수': post_var,
                    '사전 평균': pre_data.mean(),
                    '사후 평균': post_data.mean(),
                    '사전 표준편차': pre_data.std(),
                    '사후 표준편차': post_data.std(),
                    't-값': t_stat,
                    'p-값': p_value,
                    '유의성': 'p < .05' if p_value < 0.05 else 'N.S.' # Not Significant
                })

            if results:
                # --- 분석 결과 표 출력 ---
                st.header("📊 대응표본 t-검정 결과")
                results_df = pd.DataFrame(results)
                
                # 소수점 자리수 포맷팅
                st.dataframe(results_df.style.format({
                    '사전 평균': '{:.3f}',
                    '사후 평균': '{:.3f}',
                    '사전 표준편차': '{:.3f}',
                    '사후 표준편차': '{:.3f}',
                    't-값': '{:.3f}',
                    'p-값': '{:.3f}'
                }))
                st.info("p-값이 0.05보다 작으면 통계적으로 유의미한 차이가 있다고 해석할 수 있습니다.")

                # --- 5. 데이터 시각화 ---
                st.header("📈 시각화 자료")
                
                # 각 변수 쌍에 대해 차트 생성
                for index, row in results_df.iterrows():
                    pre_var = row['사전 변수']
                    post_var = row['사후 변수']
                    
                    st.subheader(f"'{pre_var}' vs '{post_var}' 분석")
                    
                    # 시각화를 위한 컬럼 레이아웃
                    chart_col1, chart_col2 = st.columns(2)
                    
                    # Raincloud Plot
                    with chart_col1:
                        pre_df_plot = pd.DataFrame({'점수': df[pre_var], '시점': f'사전 ({pre_var})'})
                        post_df_plot = pd.DataFrame({'점수': df[post_var], '시점': f'사후 ({post_var})'})
                        plot_df = pd.concat([pre_df_plot, post_df_plot])

                        fig_rain = px.violin(
                            plot_df, y='점수', x='시점', color='시점',
                            box=True, points='all',
                            color_discrete_map={
                                f'사전 ({pre_var})': 'blue',
                                f'사후 ({post_var})': 'orange'
                            }
                        )
                        fig_rain.update_layout(
                            title_text='<b>사전-사후 분포 비교 (Raincloud Plot)</b>',
                            xaxis_title='검사 시점', yaxis_title='점수', showlegend=False
                        )
                        st.plotly_chart(fig_rain, use_container_width=True)

                    # Scatter Plot
                    with chart_col2:
                        fig_scatter = go.Figure()
                        fig_scatter.add_trace(go.Scatter(
                            x=df[pre_var], y=df[post_var], mode='markers',
                            marker=dict(color='rgba(135, 206, 250, 0.5)'), name='데이터 포인트'
                        ))
                        min_val = min(df[pre_var].min(), df[post_var].min())
                        max_val = max(df[pre_var].max(), df[post_var].max())
                        fig_scatter.add_trace(go.Scatter(
                            x=[min_val, max_val], y=[min_val, max_val], mode='lines',
                            line=dict(color='grey', dash='dash'), name='변화 없음 기준선'
                        ))
                        fig_scatter.update_layout(
                            title_text='<b>사전-사후 관계 (Scatter Plot)</b>',
                            xaxis_title=f'사전 점수 ({pre_var})', yaxis_title=f'사후 점수 ({post_var})'
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                    # Line Graph
                    fig_line = go.Figure()
                    for i in range(len(df)):
                        fig_line.add_trace(go.Scatter(
                            x=[pre_var, post_var],
                            y=[df.loc[i, pre_var], df.loc[i, post_var]],
                            mode='lines+markers', marker=dict(color='lightgrey'),
                            line=dict(width=1), showlegend=False
                        ))
                    fig_line.update_layout(
                        title_text='<b>개별 데이터 변화 추이 (Line Graph)</b>',
                        xaxis_title='검사 시점', yaxis_title='점수'
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
                    st.write("---")

else:
    # 초기 화면 안내 메시지
    st.info("👈 사이드바에서 CSV 파일을 업로드하여 분석을 시작하세요.")

# --- 6. Footer 추가 ---
# 앱의 가장 하단에 위치하도록 조건문 바깥에 배치합니다.
st.divider() # 시각적인 구분을 위한 라인
st.markdown(
    """
    <div style="text-align: center; color: grey;">
        © 2025 이대형. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)