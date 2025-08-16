import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# --------------------
# 多语言字典
# --------------------
LANG = {
    "中文": {
        "title": "五位数热号图 终极版",
        "recent_periods": "选择最近多少期生成热号图",
        "chart_type": "选择图表类型",
        "bar_chart": "柱状图（首位热号）",
        "heatmap": "热力图（每位数字热号）",
        "pie_chart": "饼图 / 圆环图（首位数字占比）",
        "plotly_chart": "交互式 Plotly 柱状图（首位热号）",
        "first_digit_stats": "首位数字热号统计（最近 {n} 期）",
        "bar_title": "首位数字热号柱状图",
        "bar_xlabel": "首位数字",
        "bar_ylabel": "出现次数",
        "heat_title": "五位数每位数字热力图",
        "pie_title": "首位数字占比",
        "plotly_title": "首位数字热号 (交互式)",
        "read_error": "无法读取 history.csv，请确认文件存在并且编码为 UTF-8 / UTF-16 / GBK",
        "read_success": "历史数据读取成功！",
        "csv_columns_error": "CSV 文件必须包含 '期号' 和 'number' 两列",
    },
    "English": {
        "title": "5-Digit Hot Number Chart MVP",
        "recent_periods": "Select number of recent periods",
        "chart_type": "Select chart type",
        "bar_chart": "Bar Chart (First Digit Hot)",
        "heatmap": "Heatmap (All Digits)",
        "pie_chart": "Pie / Donut Chart (First Digit)",
        "plotly_chart": "Interactive Plotly Bar (First Digit Hot)",
        "first_digit_stats": "First Digit Hot Stats (Last {n} periods)",
        "bar_title": "First Digit Hot Bar Chart",
        "bar_xlabel": "First Digit",
        "bar_ylabel": "Count",
        "heat_title": "5-Digit Heatmap",
        "pie_title": "First Digit Share",
        "plotly_title": "First Digit Hot (Interactive)",
        "read_error": "Cannot read history.csv, please check the file exists and encoding is UTF-8 / UTF-16 / GBK",
        "read_success": "History data loaded successfully!",
        "csv_columns_error": "CSV must contain '期号' and 'number' columns",
    },
    "ລາວ": {  # 老挝文
        "title": "ແຜນລາຍການຕົວເລກຮ້ອນ 5 ໂຕ",
        "recent_periods": "ເລືອກຈຳນວນສຸດທ້າຍຂອງລາຍການຕິດຕາມ",
        "chart_type": "ເລືອກປະເພດການສ້າງແຜນ",
        "bar_chart": "ແຜນຖັງທາງລາຍການຕົວເລກຕົ້ນ",
        "heatmap": "ແຜນຮ້ອນ (ທຸກຕົວເລກ)",
        "pie_chart": "ແຜນພິກ / ແຜນວົງກົງ (ຕົວເລກຕົ້ນ)",
        "plotly_chart": "ແຜນ Plotly ອິນເຕີແກຕິບ (ຕົວເລກຕົ້ນ)",
        "first_digit_stats": "ສະຖິຕິຕົວເລກຕົ້ນ (ສຸດທ້າຍ {n} ລາຍການ)",
        "bar_title": "ແຜນຖັງຕົວເລກຕົ້ນ",
        "bar_xlabel": "ຕົວເລກຕົ້ນ",
        "bar_ylabel": "ຈຳນວນ",
        "heat_title": "ແຜນຮ້ອນ 5 ໂຕ",
        "pie_title": "ສ່ວນຕົວເລກຕົ້ນ",
        "plotly_title": "ຕົວເລກຕົ້ນ (ອິນເຕີແກຕິບ)",
        "read_error": "ບໍ່ສາມາດອ່ານ history.csv ກະລຸນາກວດຊອບໄຟລ໌ ແລະ ການລະຫັດ UTF-8 / UTF-16 / GBK",
        "read_success": "ຂໍ້ມູນປະຫວັດ ຖືກເກັບໄວ້ແລ້ວ!",
        "csv_columns_error": "CSV ຈຳເປັນຕ້ອງມີ 'ລາຍການ' ແລະ 'number'",
    },
    "ไทย": {  # 泰文
        "title": "กราฟเลขร้อน 5 หลัก",
        "recent_periods": "เลือกจำนวนงวดล่าสุด",
        "chart_type": "เลือกประเภทกราฟ",
        "bar_chart": "กราฟแท่ง (ตัวเลขหลักแรก)",
        "heatmap": "กราฟฮีทแมป (ทุกหลัก)",
        "pie_chart": "กราฟวงกลม / แหวน (ตัวเลขหลักแรก)",
        "plotly_chart": "กราฟ Plotly แบบโต้ตอบ (ตัวเลขหลักแรก)",
        "first_digit_stats": "สถิติเลขหลักแรก (ย้อนหลัง {n} งวด)",
        "bar_title": "กราฟแท่งเลขหลักแรก",
        "bar_xlabel": "เลขหลักแรก",
        "bar_ylabel": "จำนวนครั้ง",
        "heat_title": "กราฟฮีทแมป 5 หลัก",
        "pie_title": "สัดส่วนเลขหลักแรก",
        "plotly_title": "เลขหลักแรก (โต้ตอบได้)",
        "read_error": "ไม่สามารถอ่านไฟล์ history.csv กรุณาตรวจสอบไฟล์และรหัส UTF-8 / UTF-16 / GBK",
        "read_success": "โหลดข้อมูลประวัติเรียบร้อย!",
        "csv_columns_error": "CSV ต้องมีคอลัมน์ '期号' และ 'number'",
    }
}

# --------------------
# 页面顶部语言选择
# --------------------
lang_choice = st.selectbox("选择语言 / Select Language / ເລືອກພາສາ / เลือกภาษา", list(LANG.keys()))
T = LANG[lang_choice]

st.title(T["title"])

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
    st.error(T["read_error"])
else:
    if "期号" not in df.columns or "number" not in df.columns:
        st.error(T["csv_columns_error"])
    else:
        st.success(T["read_success"])

        # --------------------
        # 最近多少期
        # --------------------
        total_periods = len(df)
        n_recent = st.slider(T["recent_periods"], 
                             min_value=10, 
                             max_value=total_periods, 
                             value=50)
        df_range = df.head(n_recent).copy()  # 取最新的 n_recent 期

        # --------------------
        # 提取首位数字（保持字符串，避免丢失 0）
        # --------------------
        df_range["first_digit"] = df_range["number"].astype(str).str[0]
        first_digit_counts = df_range["first_digit"].value_counts().sort_index()

        st.subheader(T["first_digit_stats"].format(n=n_recent))
        st.write(first_digit_counts)

        # --------------------
        # 选择图表类型
        # --------------------
        chart_type = st.selectbox(T["chart_type"], [
            T["bar_chart"],
            T["heatmap"],
            T["pie_chart"],
            T["plotly_chart"]
        ])

        if chart_type == T["bar_chart"]:
            plt.figure(figsize=(6,4))
            sns.barplot(x=first_digit_counts.index, y=first_digit_counts.values, palette="Reds_d")
            plt.title(T["bar_title"])
            plt.xlabel(T["bar_xlabel"])
            plt.ylabel(T["bar_ylabel"])
            for i, v in enumerate(first_digit_counts.values):
                plt.text(i, v + 0.05, str(int(v)), ha='center', va='bottom', fontsize=9)
            st.pyplot(plt)

        elif chart_type == T["heatmap"]:
            digits_df = df_range["number"].astype(str).apply(lambda x: list(x))
            digits_df = pd.DataFrame(digits_df.tolist(), columns=["位1","位2","位3","位4","位5"])
            heat_counts = digits_df.apply(lambda col: col.value_counts().sort_index()).fillna(0)

            plt.figure(figsize=(6,4))
            sns.heatmap(heat_counts, annot=True, cmap="Reds", fmt=".0f")
            plt.title(T["heat_title"])
            st.pyplot(plt)

        elif chart_type == T["pie_chart"]:
            plt.figure(figsize=(5,5))
            plt.pie(first_digit_counts.values, labels=first_digit_counts.index,
                    autopct="%1.1f%%", startangle=90, wedgeprops={'width':0.4})
            plt.title(T["pie_title"])
            st.pyplot(plt)

        elif chart_type == T["plotly_chart"]:
            count_df = first_digit_counts.reset_index()
            count_df.columns = ["digit","count"]
            fig = px.bar(count_df, x="digit", y="count", color="count", 
                         color_continuous_scale="Reds", title=T["plotly_title"])
            st.plotly_chart(fig)
