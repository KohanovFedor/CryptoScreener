import streamlit as st
from lightweight_charts import Chart
import pandas as pd

def render_mini_charts(df_dict: dict, cols_per_row: int = 5):
    """
    Отображает мини-графики по 5 в ряд.
    df_dict: {symbol: DataFrame}
    """
    symbols = list(df_dict.keys())
    
    if not symbols:
        st.warning("Нет данных для отображения")
        return

    # Создаём строки по cols_per_row графиков
    for i in range(0, len(symbols), cols_per_row):
        row_symbols = symbols[i:i + cols_per_row]
        cols = st.columns(len(row_symbols))
        
        for col, symbol in zip(cols, row_symbols):
            with col:
                st.markdown(f"**{symbol}**")
                df = df_dict[symbol]
                if df.empty:
                    st.caption("Нет данных")
                    continue
                
                # Создаём чарт
                chart = Chart(width=250, height=200, inner_width=1.0, inner_height=1.0)
                chart.set(df)
                chart.show()