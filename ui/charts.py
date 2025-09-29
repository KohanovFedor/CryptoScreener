# ui/charts.py
import streamlit as st
from streamlit_lightweight_charts_pro.charts import Chart
from streamlit_lightweight_charts_pro.charts.series.candlestick import CandlestickSeries
from streamlit_lightweight_charts_pro.charts.options import ChartOptions
from streamlit_lightweight_charts_pro.charts.options.price_format_options import PriceFormatOptions

def render_mini_charts(df_dict: dict, cols_per_row: int = 5):
    symbols = list(df_dict.keys())
    if not symbols:
        st.warning("Нет данных для отображения")
        return

    # Отображаем по 5 в ряд
    for i in range(0, len(symbols), cols_per_row):
        row_symbols = symbols[i:i + cols_per_row]
        cols = st.columns(len(row_symbols))
        cols = st.columns(5)
        for col, symbol in zip(cols, row_symbols):
            with col:
                st.markdown(f"**{symbol}**")
                df = df_dict[symbol]["data"]
                
                # Подготавливаем данные в формате для библиотеки
                # Библиотека ожидает список словарей с time, open, high, low, close
                candlestick_series_df = CandlestickSeries(
                    data=df,
                    column_mapping={
                        "time": "time",
                        "open": "open",
                        "high": "high",
                        "low": "low",
                        "close": "close",
                    },
                )
                precision = df_dict[symbol]["precision"]
                price_format = PriceFormatOptions(type="price", precision=precision, min_move=pow(0.1, precision))
                candlestick_series_df._price_format = price_format
                chart = Chart(series=candlestick_series_df, options=ChartOptions(width=300, height=200))
                chart.render(key=f"chart_{symbol}")