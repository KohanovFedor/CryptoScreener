import streamlit as st
from exchanges.mexc import MEXCExchange
from ui.charts import render_mini_charts
import pandas as pd

# === КЭШИРОВАНИЕ ДАННЫХ ===
@st.cache_data(ttl=300)  # кэш на 5 минут
def fetch_exchange_data(exchange_name: str, interval: str, limit: int):
    if exchange_name == "MEXC":
        exchange = MEXCExchange()
    else:
        st.error("Неподдерживаемая биржа")
        return {}, []

    try:
        symbols = exchange.get_symbols()
        st.write(f"✅ Загружено {len(symbols)} символов")
    except Exception as e:
        st.error(f"Ошибка при загрузке списка символов: {e}")
        return {}, []

    df_dict = {}
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, symbol in enumerate(symbols):
        status_text.text(f"Загрузка {symbol} ({i+1}/{len(symbols)})")
        try:
            df = exchange.get_klines(symbol, interval=interval, limit=limit)
            if not df.empty and len(df) > 1:
                df_dict[symbol] = df
        except Exception as e:
            st.warning(f"Пропущен {symbol}: {e}")
        progress_bar.progress((i + 1) / len(symbols))

    status_text.empty()
    progress_bar.empty()
    return df_dict, symbols

# === ИНТЕРФЕЙС ===
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
    limit = st.slider("Количество свечей", 20, 200, 100)

# Запуск загрузки только при нажатии кнопки (или автоматически)
if st.button("Загрузить данные") or 'df_dict' in st.session_state:
    with st.spinner("Подготовка данных..."):
        df_dict, symbols = fetch_exchange_data(exchange_choice, interval, limit)

    if df_dict:
        st.subheader(f"📈 {exchange_choice} — отображено {len(df_dict)} графиков")
        render_mini_charts(df_dict, cols_per_row=5)
        st.caption("Прокручивайте вниз, чтобы увидеть все графики")
    else:
        st.warning("Не удалось загрузить ни одного графика. Проверьте подключение к API.")