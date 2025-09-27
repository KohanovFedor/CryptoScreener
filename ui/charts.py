# ui/charts.py
import streamlit as st
from streamlit.components.v1 import html
import json

def render_mini_charts(df_dict: dict, cols_per_row: int = 5):
    """
    Отображает мини-графики с помощью Lightweight Charts через HTML/JS.
    df_dict: {symbol: DataFrame с колонками time, open, high, low, close, volume}
    """
    symbols = list(df_dict.keys())
    if not symbols:
        st.warning("Нет данных для отображения")
        return

    # Преобразуем все DataFrame в JSON
    charts_data = {}
    for symbol, df in df_dict.items():
        if df.empty:
            continue
        # Lightweight Charts требует time в секундах (у вас уже так!)
        records = df[["time", "open", "high", "low", "close", "volume"]].to_dict(orient="records")
        charts_data[symbol] = records

    if not charts_data:
        st.warning("Нет валидных данных для графиков")
        return

    # Разбиваем на строки
    symbol_items = list(charts_data.items())
    for i in range(0, len(symbol_items), cols_per_row):
        row = symbol_items[i:i + cols_per_row]
        
        # Создаём контейнер для строки
        cols = st.columns(len(row))
        for col, (symbol, data) in zip(cols, row):
            with col:
                st.markdown(f"**{symbol}**")
                # Генерируем HTML для одного чарта
                chart_html = _generate_chart_html(data, width=250, height=200)
                html(chart_html, height=220, scrolling=False)

def _generate_chart_html(data, width=250, height=200):
    """Генерирует HTML+JS для одного Lightweight Chart"""
    data_json = json.dumps(data)
    return f"""
    <div>
        <div id="chart" style="width:{width}px; height:{height}px;"></div>
    </div>
    <script type="text/javascript" src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <script type="text/javascript">
        // Создаём чарт
        const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
            width: {width},
            height: {height},
            layout: {{
                backgroundColor: '#ffffff',
                textColor: '#333',
            }},
            grid: {{
                vertLines: {{ color: '#f0f0f0' }},
                horzLines: {{ color: '#f0f0f0' }},
            }},
            crosshair: {{ mode: LightweightCharts.CrosshairMode.Normal }},
            priceScale: {{ borderColor: '#ccc' }},
            timeScale: {{ borderColor: '#ccc', timeVisible: true }}
        }});

        // Добавляем серию свечей
        const candleSeries = chart.addCandlestickSeries({{
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350',
        }});

        // Устанавливаем данные
        candleSeries.setData({data_json});
        
        // Автомасштаб
        chart.timeScale().fitContent();
    </script>
    """