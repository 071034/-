import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

st.title("五位数热号图 终极版")

# --------------------
# 自动读取 history.csv，支持多种编码
# --------------------
file_path = "history.csv"
encodings_to_try = ["utf-8-sig", "utf-16", "gbk"]

df = None
for enc in encodings_to_try:
    try:
        df = pd.read_csv(file_path, encoding=enc, dtype={"期号": str, "number": str})
        break
    except Exception:
        continue

if df is None:
    st.error("无法读取 history.csv，请确认文件存在并且编码为 UTF-8 / UTF-16 / GBK")
else:
    if "期号" not in df.columns or "number" not in df.columns:
        st.error("CSV 文件必须包含 '期号' 和 'number' 两列")
    else:
        st.success("历史数据读取成功！")

        # --------------------
        # 最近多少期
        # --------------------
        total_periods = len(df)
        n_recent = st.slider("选择最近多少期生成热号图", 
                             min_value=10, 
                             max_value=total_periods, 
                             value=50)
        df_range = df.head(n_recent).copy()  # 取最新的 n_recent 期

        # --------------------
        # 提取首位数字（保持字符串，避免丢失 0）
        # --------------------
        df_range["first_digit"] = df_range["number"].astype(str).str[0]
        first_digit_counts = df_range["first_digit"].value_counts().sort_index()

        st.subheader(f"首位数字热号统计（最近 {n_recent} 期）")
        st.write(first_digit_counts)

        # --------------------
        # 选择图表类型
        # --------------------
        chart_type = st.selectbox("选择图表类型", [
            "柱状图（首位热号）",
            "热力图（每位数字热号）",
            "饼图 / 圆环图（首位数字占比）",
            "交互式 Plotly 柱状图（首位热号）"
        ])

        if chart_type == "柱状图（首位热号）":
            plt.figure(figsize=(6,4))
            sns.barplot(x=first_digit_counts.index, y=first_digit_counts.values, palette="Reds_d")
            plt.title("首位数字热号柱状图")
            plt.xlabel("首位数字")
            plt.ylabel("出现次数")
            for i, v in enumerate(first_digit_counts.values):
                plt.text(i, v + 0.05, str(int(v)), ha='center', va='bottom', fontsize=9)
            st.pyplot(plt)

        elif chart_type == "热力图（每位数字热号）":
            digits_df = df_range["number"].astype(str).apply(lambda x: list(x))
            digits_df = pd.DataFrame(digits_df.tolist(), columns=["位1","位2","位3","位4","位5"])
            heat_counts = digits_df.apply(lambda col: col.value_counts().sort_index()).fillna(0)

            plt.figure(figsize=(6,4))
            sns.heatmap(heat_counts, annot=True, cmap="Reds", fmt=".0f")
            plt.title("五位数每位数字热力图")
            st.pyplot(plt)

        elif chart_type == "饼图 / 圆环图（首位数字占比）":
            plt.figure(figsize=(5,5))
            plt.pie(first_digit_counts.values, labels=first_digit_counts.index,
                    autopct="%1.1f%%", startangle=90, wedgeprops={'width':0.4})
            plt.title("首位数字占比")
            st.pyplot(plt)

        elif chart_type == "交互式 Plotly 柱状图（首位热号）":
            count_df = first_digit_counts.reset_index()
            count_df.columns = ["digit","count"]
            fig = px.bar(count_df, x="digit", y="count", color="count", 
                         color_continuous_scale="Reds", title="首位数字热号 (交互式)")
            st.plotly_chart(fig)
