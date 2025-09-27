import streamlit as st
from exchanges.mexc import MEXCExchange
from ui.charts import render_mini_charts
import pandas as pd

# Настройки
st.set_page_config(
    page_title="Multi-Exchange Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Multi-Exchange Candlestick Dashboard")

# Боковая панель
with st.sidebar:
    st.header("Настройки")
    exchange_choice = st.selectbox("Биржа", ["MEXC"])
    interval = st.selectbox("Интервал", ["15m", "1h", "4h", "1d"], index=3)
    limit = st.slider("Количество свечей", 50, 500, 100)

# Инициализация биржи
exchange = MEXCExchange()

# Загрузка символов
with st.spinner("Загрузка списка инструментов..."):
    symbols = exchange.get_symbols()

st.subheader(f"📈 {exchange.name} — {len(symbols)} инструментов")

# Загрузка данных для всех символов
df_dict = {}
with st.spinner("Загрузка свечных данных..."):
    for symbol in symbols:
        df = exchange.get_klines(symbol, interval=interval, limit=limit)
        df_dict[symbol] = df

# Отображение графиков
render_mini_charts(df_dict, cols_per_row=5)

st.caption("Прокручивайте вниз, чтобы увидеть все графики")