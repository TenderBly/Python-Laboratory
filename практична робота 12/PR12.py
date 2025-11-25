import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys

#імпорт та підготовка даних
def get_user_input():
    """
    Функція для взаємодії з користувачем та отримання параметрів аналізу.
    
    Returns:
        dict: Словник з параметрами (тикери, період, тип аналізу)
    """
    print("=" * 70)
    print("ПРОГРАМА АНАЛІЗУ ФІНАНСОВИХ ПОКАЗНИКІВ")
    print("=" * 70)
    print("\nДоступні режими роботи:")
    print("1 - Аналіз акцій")
    print("2 - Аналіз валютних пар")
    print("3 - Порівняльний аналіз декількох активів")
    print("4 - Аналіз з власними даними продажів")
    
    while True:
        try:
            mode = int(input("\nОберіть режим (1-4): "))
            if mode not in [1, 2, 3, 4]:
                raise ValueError
            break
        except ValueError:
            print(" Помилка! Введіть число від 1 до 4.")
    
    # Отримання тикерів залежно від режиму
    if mode == 1:
        print("\nПриклади акцій: AAPL (Apple), GOOGL (Google), MSFT (Microsoft), AMZN (Amazon), TSLA (Tesla), META (Meta Platforms), NVDA (Nvidia), NFLX (Netflix), JPM (JPMorgan Chase), BAC (Bank of America)")
        tickers = input("Введіть тикер акції: ").strip().upper()
    elif mode == 2:
        print("\nПриклади валют: EURUSD=X, GBPUSD=X, USDJPY=X, USDCHF=X, AUDUSD=X, USDCAD=X, NZDUSD=X, EURGBP=X, EURJPY=X, GBPJPY=X")
        tickers = input("Введіть валютну пару: ").strip().upper()
    elif mode == 3:
        print("\nВведіть тикери через кому (наприклад: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, NFLX, JPM, BAC)")
        tickers = input("Тикери: ").strip().upper()
    else:
        tickers = "CUSTOM"
    
    # Вибір періоду
    print("\nДоступні періоди:")
    print("1 - Останній тиждень (7 днів)")
    print("2 - Останній місяць (30 днів)")
    print("3 - Останні 3 місяці")
    print("4 - Останній рік")
    print("5 - Власний період")
    
    while True:
        try:
            period_choice = int(input("\nОберіть період (1-5): "))
            if period_choice not in [1, 2, 3, 4, 5]:
                raise ValueError
            break
        except ValueError:
            print(" Помилка! Введіть число від 1 до 5.")
    
    # Визначення дат
    end_date = datetime.now()
    if period_choice == 1:
        start_date = end_date - timedelta(days=7)
    elif period_choice == 2:
        start_date = end_date - timedelta(days=30)
    elif period_choice == 3:
        start_date = end_date - timedelta(days=90)
    elif period_choice == 4:
        start_date = end_date - timedelta(days=365)
    else:
        while True:
            try:
                start_str = input("Введіть початкову дату (РРРР-ММ-ДД): ")
                start_date = datetime.strptime(start_str, "%Y-%m-%d")
                break
            except ValueError:
                print(" Невірний формат дати!")
    
    return {
        'mode': mode,
        'tickers': tickers,
        'start_date': start_date,
        'end_date': end_date
    }


def download_stock_data(ticker, start_date, end_date):
    """
    Завантаження даних з Yahoo Finance з обробкою помилок.
    
    Args:
        ticker (str): Тикер акції або валюти
        start_date (datetime): Початкова дата
        end_date (datetime): Кінцева дата
    
    Returns:
        pd.DataFrame: DataFrame з історичними даними або None при помилці
    """
    try:
        print(f"\n Завантаження даних для {ticker}...")
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if data.empty:
            print(f"  Попередження: Дані для {ticker} не знайдено!")
            return None
        
        # ВИПРАВЛЕННЯ: Якщо колонки мають мультііндекс, спрощуємо їх
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        print(f" Завантажено {len(data)} записів для {ticker}")
        return data
    
    except Exception as e:
        print(f" Помилка завантаження даних для {ticker}: {str(e)}")
        return None


def load_custom_sales_data():
    """
    Завантаження власних даних продажів з CSV файлу.
    Створює приклад файлу, якщо він не існує.
    
    Returns:
        pd.DataFrame: DataFrame з даними продажів або None
    """
    filename = "sales_data.csv"
    
    if not os.path.exists(filename):
        print(f"\n Файл {filename} не знайдено. Створюю приклад...")
        
        # Створення прикладу даних
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        sample_data = pd.DataFrame({
            'Date': dates,
            'Sales': [1000 + i*50 + (i%7)*100 for i in range(30)],
            'Product': ['Товар A' if i%2==0 else 'Товар B' for i in range(30)]
        })
        sample_data.to_csv(filename, index=False, encoding='utf-8')
        print(f" Створено файл прикладу: {filename}")
    
    try:
        data = pd.read_csv(filename, encoding='utf-8')
        data['Date'] = pd.to_datetime(data['Date'])
        print(f" Завантажено {len(data)} записів з {filename}")
        return data
    
    except Exception as e:
        print(f" Помилка читання файлу {filename}: {str(e)}")
        return None


#обробка та аналіз даних
def clean_and_prepare_data(data):
    """
    Очищення та підготовка даних: видалення пропусків, конвертація типів.
    
    Args:
        data (pd.DataFrame): Вхідні дані
    
    Returns:
        pd.DataFrame: Очищені дані
    """
    print("\n Очищення даних...")
    
    # Видалення рядків з пропусками
    initial_rows = len(data)
    data = data.dropna()
    removed_rows = initial_rows - len(data)
    
    if removed_rows > 0:
        print(f"  Видалено {removed_rows} рядків з пропусками")
    
    # ВИПРАВЛЕННЯ: НЕ скидаємо індекс, щоб зберегти дати в індексі
    # data = data.reset_index()
    
    print(f" Дані очищено. Залишилось {len(data)} записів")
    return data


def calculate_statistics(data, ticker):
    """
    Розрахунок статистичних показників для фінансових даних.
    
    Args:
        data (pd.DataFrame): Дані акцій/валют
        ticker (str): Назва тикера
    
    Returns:
        dict: Словник зі статистичними показниками
    """
    print(f"\n Розрахунок статистики для {ticker}...")
    
    try:
        # ВИПРАВЛЕННЯ: Використовуємо .index для доступу до дат
        stats = {
            'ticker': ticker,
            'start_date': data.index[0].strftime('%Y-%m-%d'),
            'end_date': data.index[-1].strftime('%Y-%m-%d'),
            'start_price': float(data['Close'].iloc[0]),
            'end_price': float(data['Close'].iloc[-1]),
            'min_price': float(data['Close'].min()),
            'max_price': float(data['Close'].max()),
            'avg_price': float(data['Close'].mean()),
            'std_dev': float(data['Close'].std()),
            'total_change': float(data['Close'].iloc[-1] - data['Close'].iloc[0]),
            'percent_change': float((data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100),
            'avg_volume': float(data['Volume'].mean()) if 'Volume' in data.columns else 0
        }
        
        print(f" Статистика розрахована:")
        print(f"   • Зміна ціни: {stats['percent_change']:.2f}%")
        print(f"   • Мін/Макс: ${stats['min_price']:.2f} / ${stats['max_price']:.2f}")
        
        return stats
    
    except Exception as e:
        print(f" Помилка розрахунку статистики: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def calculate_moving_averages(data, windows=[7, 30]):
    """
    Розрахунок ковзних середніх для технічного аналізу.
    
    Args:
        data (pd.DataFrame): Дані з цінами
        windows (list): Періоди для ковзних середніх
    
    Returns:
        pd.DataFrame: Дані з доданими ковзними середніми
    """
    print("\n Розрахунок ковзних середніх...")
    
    try:
        for window in windows:
            col_name = f'MA_{window}'
            data[col_name] = data['Close'].rolling(window=window).mean()
            print(f"   • Додано MA({window})")
        
        return data
    
    except Exception as e:
        print(f" Помилка розрахунку ковзних середніх: {str(e)}")
        return data


#візуалізація даних
def create_price_chart(data, ticker, stats):
    """
    Створення інтерактивної діаграми цін з ковзними середніми.
    
    Args:
        data (pd.DataFrame): Дані з цінами
        ticker (str): Назва тикера
        stats (dict): Статистичні показники
    
    Returns:
        plotly.graph_objects.Figure: Об'єкт графіка
    """
    print(f"\n Створення графіка для {ticker}...")
    
    try:
        fig = go.Figure()
        
        # Основна лінія ціни закриття
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Ціна закриття',
            line=dict(color='#2E86DE', width=2),
            hovertemplate='Дата: %{x}<br>Ціна: $%{y:.2f}<extra></extra>'
        ))
        
        # Додавання ковзних середніх
        if 'MA_7' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA_7'],
                mode='lines',
                name='MA(7)',
                line=dict(color='#10AC84', width=1, dash='dash'),
                hovertemplate='MA(7): $%{y:.2f}<extra></extra>'
            ))
        
        if 'MA_30' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA_30'],
                mode='lines',
                name='MA(30)',
                line=dict(color='#EE5A6F', width=1, dash='dot'),
                hovertemplate='MA(30): $%{y:.2f}<extra></extra>'
            ))
        
        # Налаштування макету
        fig.update_layout(
            title=f'Динаміка ціни {ticker}<br><sub>Зміна: {stats["percent_change"]:.2f}%</sub>',
            xaxis_title='Дата',
            yaxis_title='Ціна (USD)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            font=dict(size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        print(" Графік створено")
        return fig
    
    except Exception as e:
        print(f" Помилка створення графіка: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def create_volume_chart(data, ticker):
    """
    Створення діаграми обсягів торгів.
    
    Args:
        data (pd.DataFrame): Дані з обсягами
        ticker (str): Назва тикера
    
    Returns:
        plotly.graph_objects.Figure: Об'єкт графіка
    """
    if 'Volume' not in data.columns:
        print(f"\n  Обсяги торгів недоступні для {ticker}")
        return None
    
    # Перевірка, чи є реальні дані про обсяги
    if data['Volume'].sum() == 0 or data['Volume'].isna().all():
        print(f"\n  Обсяги торгів для {ticker} порожні (це нормально для валютних пар)")
        return None
    
    print(f"\n Створення графіка обсягів для {ticker}...")
    
    try:
        fig = go.Figure()
        
        # Визначення кольорів стовпців (зелений - зростання, червоний - падіння)
        colors = ['green' if data['Close'].iloc[i] >= data['Close'].iloc[i-1] 
                  else 'red' for i in range(1, len(data))]
        colors.insert(0, 'gray')  # Перший елемент
        
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Обсяг',
            marker=dict(color=colors, opacity=0.7),
            hovertemplate='Дата: %{x}<br>Обсяг: %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Обсяг торгів {ticker}',
            xaxis_title='Дата',
            yaxis_title='Обсяг',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        print(" Графік обсягів створено")
        return fig
    
    except Exception as e:
        print(f" Помилка створення графіка обсягів: {str(e)}")
        return None


def create_comparison_chart(data_dict):
    """
    Створення порівняльної діаграми для декількох активів.
    
    Args:
        data_dict (dict): Словник з даними для кожного тикера
    
    Returns:
        plotly.graph_objects.Figure: Об'єкт графіка
    """
    print("\n Створення порівняльної діаграми...")
    
    try:
        fig = go.Figure()
        
        colors = ['#2E86DE', '#10AC84', '#EE5A6F', '#FD79A8', '#6C5CE7']
        
        for idx, (ticker, data) in enumerate(data_dict.items()):
            # Нормалізація до відсотків (базова дата = 100%)
            normalized = (data['Close'] / data['Close'].iloc[0] * 100)
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=normalized,
                mode='lines',
                name=ticker,
                line=dict(color=colors[idx % len(colors)], width=2),
                hovertemplate=f'{ticker}<br>%{{y:.2f}}%<extra></extra>'
            ))
        
        fig.update_layout(
            title='Порівняльна динаміка активів (нормалізовано до 100%)',
            xaxis_title='Дата',
            yaxis_title='Відносна зміна (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        print(" Порівняльний графік створено")
        return fig
    
    except Exception as e:
        print(f" Помилка створення порівняльного графіка: {str(e)}")
        return None


def create_sales_chart(data):
    """
    Створення діаграми продажів з власних даних.
    
    Args:
        data (pd.DataFrame): Дані продажів
    
    Returns:
        plotly.graph_objects.Figure: Об'єкт графіка
    """
    print("\n Створення діаграми продажів...")
    
    try:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Динаміка продажів', 'Продажі по продуктах'),
            vertical_spacing=0.15,
            row_heights=[0.6, 0.4]
        )
        
        # Графік динаміки
        fig.add_trace(
            go.Scatter(
                x=data['Date'],
                y=data['Sales'],
                mode='lines+markers',
                name='Продажі',
                line=dict(color='#2E86DE', width=2),
                marker=dict(size=6),
                hovertemplate='Дата: %{x}<br>Продажі: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Діаграма по продуктах
        if 'Product' in data.columns:
            product_sales = data.groupby('Product')['Sales'].sum().reset_index()
            
            fig.add_trace(
                go.Bar(
                    x=product_sales['Product'],
                    y=product_sales['Sales'],
                    name='За продуктами',
                    marker=dict(color=['#10AC84', '#EE5A6F']),
                    hovertemplate='%{x}<br>Загальні продажі: %{y}<extra></extra>'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title='Аналіз продажів',
            template='plotly_white',
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Дата", row=1, col=1)
        fig.update_yaxes(title_text="Обсяг продажів", row=1, col=1)
        fig.update_xaxes(title_text="Продукт", row=2, col=1)
        fig.update_yaxes(title_text="Загальний обсяг", row=2, col=1)
        
        print(" Діаграма продажів створена")
        return fig
    
    except Exception as e:
        print(f" Помилка створення діаграми продажів: {str(e)}")
        return None


#збереження результатів
def save_statistics_to_file(stats_list, filename='statistics_report.txt'):
    """
    Збереження статистичного звіту у текстовий файл.
    
    Args:
        stats_list (list): Список словників зі статистикою
        filename (str): Ім'я файлу для збереження
    """
    print(f"\n Збереження статистики у файл {filename}...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("СТАТИСТИЧНИЙ ЗВІТ ФІНАНСОВОГО АНАЛІЗУ\n")
            f.write(f"Дата створення: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            for stats in stats_list:
                if stats:
                    f.write(f"Актив: {stats['ticker']}\n")
                    f.write(f"Період: {stats['start_date']} — {stats['end_date']}\n")
                    f.write(f"Початкова ціна: ${stats['start_price']:.2f}\n")
                    f.write(f"Кінцева ціна: ${stats['end_price']:.2f}\n")
                    f.write(f"Мінімальна ціна: ${stats['min_price']:.2f}\n")
                    f.write(f"Максимальна ціна: ${stats['max_price']:.2f}\n")
                    f.write(f"Середня ціна: ${stats['avg_price']:.2f}\n")
                    f.write(f"Стандартне відхилення: ${stats['std_dev']:.2f}\n")
                    f.write(f"Загальна зміна: ${stats['total_change']:.2f}\n")
                    f.write(f"Процентна зміна: {stats['percent_change']:.2f}%\n")
                    if stats['avg_volume'] > 0:
                        f.write(f"Середній обсяг: {stats['avg_volume']:,.0f}\n")
                    f.write("\n" + "-" * 70 + "\n\n")
        
        print(f" Статистику збережено у {filename}")
    
    except Exception as e:
        print(f" Помилка збереження файлу: {str(e)}")


def save_data_to_csv(data, ticker, filename=None):
    """
    Збереження оброблених даних у CSV файл.
    
    Args:
        data (pd.DataFrame): Дані для збереження
        ticker (str): Назва тикера
        filename (str): Ім'я файлу (опціонально)
    """
    if filename is None:
        filename = f"{ticker}_data_{datetime.now().strftime('%Y%m%d')}.csv"
    
    print(f"\n Збереження даних у CSV файл {filename}...")
    
    try:
        data.to_csv(filename, encoding='utf-8')
        print(f" Дані збережено у {filename}")
    
    except Exception as e:
        print(f" Помилка збереження CSV: {str(e)}")


def save_chart_to_html(fig, filename):
    """
    Збереження інтерактивного графіка у HTML файл.
    
    Args:
        fig (plotly.graph_objects.Figure): Графік для збереження
        filename (str): Ім'я файлу
    """
    if fig is None:
        return
    
    print(f"\n Збереження графіка у файл {filename}...")
    
    try:
        fig.write_html(filename)
        print(f" Графік збережено у {filename}")
    
    except Exception as e:
        print(f" Помилка збереження HTML: {str(e)}")


#main тобто головна функція
def main():
    """
    Головна функція програми, що координує всі етапи обробки.
    """
    try:
        # Етап 1: Отримання параметрів від користувача
        params = get_user_input()
        
        # Етап 2: Завантаження даних
        if params['mode'] == 4:
            # Режим власних даних продажів
            sales_data = load_custom_sales_data()
            if sales_data is None:
                print("\n Не вдалось завантажити дані продажів!")
                return
            
            # Візуалізація
            fig = create_sales_chart(sales_data)
            if fig:
                fig.show()
                save_chart_to_html(fig, 'sales_analysis.html')
                save_data_to_csv(sales_data, 'SALES', 'sales_processed.csv')
        
        elif params['mode'] == 3:
            # Режим порівняльного аналізу
            tickers = [t.strip() for t in params['tickers'].split(',')]
            data_dict = {}
            stats_list = []
            
            for ticker in tickers:
                data = download_stock_data(ticker, params['start_date'], params['end_date'])
                if data is not None:
                    data = clean_and_prepare_data(data)
                    data = calculate_moving_averages(data)
                    data_dict[ticker] = data
                    
                    stats = calculate_statistics(data, ticker)
                    if stats:
                        stats_list.append(stats)
            
            if data_dict:
                # Створення графіків
                comparison_fig = create_comparison_chart(data_dict)
                if comparison_fig:
                    comparison_fig.show()
                    save_chart_to_html(comparison_fig, 'comparison_analysis.html')
                
                # Збереження статистики
                save_statistics_to_file(stats_list, 'comparison_statistics.txt')
        
        else:
            # Режим одного активу (акція або валюта)
            ticker = params['tickers']
            data = download_stock_data(ticker, params['start_date'], params['end_date'])
            
            if data is None:
                print("\n Не вдалось завантажити дані!")
                return
            
            # Етап 3: Обробка даних
            data = clean_and_prepare_data(data)
            data = calculate_moving_averages(data)
            
            # Етап 4: Розрахунок статистики
            stats = calculate_statistics(data, ticker)
            
            if stats is None:
                print("\n Не вдалось розрахувати статистику!")
                return
            
            # Етап 5: Візуалізація
            price_fig = create_price_chart(data, ticker, stats)
            volume_fig = create_volume_chart(data, ticker)
            
            if price_fig:
                price_fig.show()
                save_chart_to_html(price_fig, f'{ticker}_price_chart.html')
            
            if volume_fig:
                volume_fig.show()
                save_chart_to_html(volume_fig, f'{ticker}_volume_chart.html')
            
            # Етап 6: Збереження результатів
            save_statistics_to_file([stats], f'{ticker}_statistics.txt')
            save_data_to_csv(data, ticker)
        
        print("\n" + "=" * 70)
        print(" ПРОГРАМА ЗАВЕРШИЛА РОБОТУ УСПІШНО!")
        print("=" * 70)
        print("\nЗбережені файли:")
        print("  • Статистичний звіт (TXT)")
        print("  • Оброблені дані (CSV)")
        print("  • Інтерактивні графіки (HTML)")
        print("\nДякуємо за використання програми!")
    
    except KeyboardInterrupt:
        print("\n\n  Програму перервано користувачем.")
    
    except Exception as e:
        print(f"\n Критична помилка: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Будь ласка, перевірте вхідні дані та спробуйте знову.")


if __name__ == "__main__":
    main()