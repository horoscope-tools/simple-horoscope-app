import streamlit as st
from kerykeion import AstrologicalSubject
from datetime import datetime

st.set_page_config(page_title="ホロスコープ詳細診断", layout="centered")
st.title("🔮 ホロスコープ詳細診断ツール")

st.markdown("生年月日・出生時間・出生地を入力して、性格・恋愛傾向・未来予測を診断します。")

# Input form
birth_date = st.date_input("生年月日")
birth_time = st.time_input("出生時間（不明ならチェック）", value=datetime(2000,1,1,12,0).time())
unknown_time = st.checkbox("出生時間が不明")
city = st.text_input("出生地（例：Tokyo）")
country = st.text_input("国コード（例：JP）", value="JP")

if st.button("🔍 診断開始"):
    try:
        hour, minute = (12, 0) if unknown_time else (birth_time.hour, birth_time.minute)
        subject = AstrologicalSubject("相談者", birth_date.year, birth_date.month, birth_date.day,
                                      hour, minute, city, country)
        natal = subject.natal_chart

        st.subheader("🧠 性格分析")
        sun = natal.planets["Sun"]
        moon = natal.planets["Moon"]
        mercury = natal.planets["Mercury"]
        venus = natal.planets["Venus"]
        mars = natal.planets["Mars"]
        asc = natal.houses["Ascendant"]

        st.markdown(f"- 🌞 太陽星座（本質）：**{sun['sign']}**（第{sun['house']}ハウス）")
        st.markdown(f"- 🌙 月星座（感情）：**{moon['sign']}**（第{moon['house']}ハウス）")
        st.markdown(f"- 🧠 水星（知性・会話）：**{mercury['sign']}**")
        st.markdown(f"- 💕 金星（恋愛）：**{venus['sign']}**（第{venus['house']}ハウス）")
        st.markdown(f"- 🔥 火星（行動力）：**{mars['sign']}**")
        st.markdown(f"- 🔼 アセンダント（第一印象）：**{asc['sign']}**")

        st.subheader("💘 恋愛傾向と魅力")
        st.write(f"金星が {venus['sign']} にあるため、恋愛では...（詳細診断）")
        st.write(f"火星が {mars['sign']} にあるため、魅力の打ち出し方は...")

        st.subheader("🔮 未来予測（トランジット）")
        today = datetime.now().strftime("%Y-%m-%d")
        transit = subject.transit_chart(today)
        venus_transit = transit.planets["Venus"]
        jupiter_transit = transit.planets["Jupiter"]

        st.write(f"金星の現在位置：{venus_transit['sign']} → 愛情運が高まりやすい日常が訪れます。")
        st.write(f"木星の現在位置：{jupiter_transit['sign']} → 発展と拡大の流れが強調されます。")

        st.success("✅ 診断完了！")

    except Exception as e:
        st.error(f"エラーが発生しました：{e}")
