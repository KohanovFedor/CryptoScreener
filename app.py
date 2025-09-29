import streamlit as st

from ui.charts import render_mini_charts
from exchanges.mexc import MEXCExchange

@st.cache_data(ttl=300)
def fetch_exchange_data(exchange_name: str, interval: str, limit: int):
    if exchange_name == "MEXC":
        exchange = MEXCExchange()
    else:
        st.error("Неподдерживаемая биржа")
        return {}

    try:
        symbols = exchange.get_symbols_from_24hr(1)
        st.write(f"✅ Загружено {len(symbols)} символов")
    except Exception as e:
        st.error(f"Ошибка при загрузке списка символов: {e.with_traceback()}")
        return {}

    df_dict = {}
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, symbol in enumerate(symbols):
        status_text.text(f"Загрузка {symbol} ({i+1}/{len(symbols)})")
        try:
            precision = 6
            df = exchange.get_klines(symbol, interval=interval, limit=limit)
            if not df.empty and len(df) > 1:
                df_dict[symbol] = {"precision": precision, "data": df}
        except Exception as e:
            st.warning(f"Пропущен {symbol}: {e}")
        progress_bar.progress((i + 1) / len(symbols))

    status_text.empty()
    progress_bar.empty()
    return df_dict

st.set_page_config(layout="wide")
st.title("📊 MEXC Dashboard — streamlit-lightweight-charts")

with st.sidebar:
    exchange = st.selectbox("Биржа", ["MEXC"])
    interval = st.selectbox("Интервал", ["1m", "5m", "15m", "30m", "1h", "4h", "1d"], index=1)
    limit = st.slider("Свечей", 20, 200, 100)

if st.button("Загрузить графики"):
    with st.spinner("Подготовка данных..."):
        df_dict = fetch_exchange_data(exchange, interval, limit)
    
    if df_dict:
        st.subheader(f"📈 {exchange} — отображено {len(df_dict)} графиков")
        render_mini_charts(df_dict, cols_per_row=5)
        st.caption("Прокручивайте вниз, чтобы увидеть все графики")
    else:
        st.warning("Не удалось загрузить ни одного графика. Проверьте подключение к API.")