from datetime import date
import numpy as np
import pandas as pd
import pickle
import psycopg2
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
import warnings
warnings.filterwarnings('ignore')
import sqlite3
import os


def streamlit_config():

    # page configuration
    st.set_page_config(page_title='Trojan Horse', layout="wide")

    # page header transparent color
    page_background_color = """
    <style> 

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">Financial Anaylsis & Management Tool</h1>',
                unsafe_allow_html=True)
    add_vertical_space(1)


# custom style for submit button - color and width

def style_submit_button():

    st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                                                        background-color: #367F89;
                                                        color: white;
                                                        width: 70%}
                    </style>
                """, unsafe_allow_html=True)


# custom style for prediction result text - color and position

def style_prediction():

    st.markdown(
        """
            <style>
            .center-text {
                text-align: center;
                color: #20CA0C
            }
            </style>
            """,
        unsafe_allow_html=True
    )


# SQL columns ditionary

def columns_dict():

    columns_dict = {'day': 'Day', 'month': 'Month', 'year': 'Year', 'store': 'Store',
                    'dept': 'Dept', 'type': 'Dept_Type', 'weekly_sales': 'Weekly_Sales',
                    'size': 'Size', 'is_holiday': 'IsHoliday', 'temperature': 'Product_Margin',
                    'fuel_price': 'Burn', 'markdown1': 'MarkDown1', 'markdown2': 'MarkDown2',
                    'markdown3': 'MarkDown3', 'markdown4': 'MarkDown4', 'markdown5': 'MarkDown5',
                    'cpi': 'CPI', 'unemployment': 'Unemployment'}
    return columns_dict



class plotly:

    def pie_chart(df, x, y, title, title_x=0.20):
        try:
            fig = px.pie(df, names=x, values=y, hole=0.5, title=title)
            fig.update_layout(title_x=title_x, title_font_size=22)
            fig.update_traces(
                textinfo='percent+value',
                textposition='outside',
                textfont=dict(color='white'),
                outsidetextfont=dict(size=14)
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating pie chart: {e}")


    def vertical_bar_chart(df, x, y, text, color, title, title_x=0.25):
        try:
            # Check if DataFrame is empty
            if df.empty:
                st.warning("No data available for the chart")
                return
                
            fig = px.bar(df, x=x, y=y, labels={x: '', y: ''}, title=title)

            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)

            fig.update_layout(title_x=title_x, title_font_size=22)

            # Convert to float if not already
            df[y] = pd.to_numeric(df[y], errors='coerce')
            
            max_val = df[y].max()
            text_position = ['inside' if val >= max_val * 0.90 else 'outside' 
                           for val in df[y]]

            fig.update_traces(marker_color=color,
                            text=df[text],
                            textposition=text_position,
                            texttemplate='%{y}',
                            textfont=dict(size=14),
                            insidetextfont=dict(color='white'),
                            textangle=0,
                            hovertemplate='%{x}<br>%{y}')

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating bar chart: {e}")


    def scatter_chart(df, x, y):

        fig = px.scatter(data_frame=df, x=x, y=y, size=y, color=y, 
                         labels={x: '', y: ''}, title=columns_dict()[x])
        
        fig.update_layout(title_x=0.4, title_font_size=22)
        
        fig.update_traces(hovertemplate=f"{x} = %{{x}}<br>{y} = %{{y}}")
        
        st.plotly_chart(fig, use_container_width=True, height=100)



class sql:

    @staticmethod
    def create_table():
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
                    day           INTEGER,
                    month         INTEGER,
                    year          INTEGER,
                    store         INTEGER,
                    dept          INTEGER,
                    type          INTEGER,
                    weekly_sales  REAL,
                    size          INTEGER,
                    is_holiday    INTEGER,
                    temperature   REAL,
                    fuel_price    REAL,
                    markdown1     REAL,
                    markdown2     REAL,
                    markdown3     REAL,
                    markdown4     REAL,
                    markdown5     REAL,
                    cpi           REAL,
                    unemployment  REAL
                )''')
                conn.commit()
                cursor.close()
                conn.close()
        except sqlite3.Error as e:
            st.error(f"Error creating table: {e}")

    @staticmethod
    def data_migration():
        try:
            # Read CSV file
            df = pd.read_csv('dataset/df_sql.csv')
            
            conn = get_db_connection()
            if conn:
                # Convert DataFrame to list of tuples
                data = df.values.tolist()
                
                # Insert data in batches
                cursor = conn.cursor()
                cursor.executemany('''
                    INSERT INTO sales VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', data)
                
                conn.commit()
                cursor.close()
                conn.close()
                
        except Exception as e:
            st.error(f"Data migration error: {e}")



class top_sales:

    @staticmethod
    def get_db_connection():
        try:
            conn = sqlite3.connect('retail_forecast.db')
            conn.row_factory = sqlite3.Row  # This enables column access by name
            return conn
        except sqlite3.Error as e:
            st.error(f"Database connection error: {e}")
            return None

    @staticmethod
    def execute_query(query, params=None):
        conn = top_sales.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
            except sqlite3.Error as e:
                st.error(f"Query error: {e}")
                return None

    @staticmethod
    def year():
        results = top_sales.execute_query(
            "SELECT DISTINCT year FROM sales ORDER BY year ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def month(year):
        if year is None:
            return []
        results = top_sales.execute_query(
            "SELECT DISTINCT month FROM sales WHERE year = ? ORDER BY month ASC",
            (year,)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def day(month, year):
        if month is None or year is None:
            return []
        results = top_sales.execute_query(
            "SELECT DISTINCT day FROM sales WHERE year = ? AND month = ? ORDER BY day ASC",
            (year, month)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def store(day, month, year):
        if any(v is None for v in [day, month, year]):
            return []
        results = top_sales.execute_query(
            """SELECT DISTINCT store FROM sales 
               WHERE day = ? AND year = ? AND month = ?
               ORDER BY store ASC""",
            (day, year, month)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def dept(day, month, year, store):
        if any(v is None for v in [day, month, year, store]):
            return []
        results = top_sales.execute_query(
            """SELECT DISTINCT dept FROM sales
               WHERE day = ? AND month = ? AND year = ? AND store = ?
               ORDER BY dept ASC""",
            (day, month, year, store)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def top_store_dept(day, month, year):
        if any(v is None for v in [day, month, year]):
            return ['Overall']
        results = top_sales.execute_query(
            """SELECT DISTINCT dept FROM sales
               WHERE day = ? AND month = ? AND year = ?
               ORDER BY dept ASC""",
            (day, month, year)
        )
        if results:
            data = [i[0] for i in results]
            data.insert(0, 'Overall')
            return data
        return ['Overall']

    @staticmethod
    def top_store_sales(condition, params=None):
        query = f"""
            SELECT store, SUM(weekly_sales) as weekly_sales
            FROM sales
            WHERE {condition}
            GROUP BY store
            ORDER BY weekly_sales DESC
            LIMIT 10
        """
        results = top_sales.execute_query(query, params)
        if results:
            index = [i for i in range(1, len(results)+1)]
            df = pd.DataFrame(results, columns=['Store', 'Weekly Sales'], index=index)
            df['Weekly Sales'] = df['Weekly Sales'].apply(lambda x: f"{x:.2f}")
            df['store_x'] = df['Store'].apply(lambda x: str(x)+'*')
            return df.rename_axis('s.no')
        return pd.DataFrame()

    @staticmethod
    def top_dept_filter_options():
        col1, col2, col3, col4 = st.columns(4, gap='medium')

        with col3:
            year = st.selectbox(label='Year  ', options=top_sales.year())

        with col2:
            month = st.selectbox(label='Month  ', options=top_sales.month(year))

        with col1:
            day = st.selectbox(label='Day  ', options=top_sales.day(month, year))

        with col4:
            store = st.selectbox(label='Store  ', options=top_sales.store(day, month, year))

        return day, month, year, store

    @staticmethod
    def top_store_filter_options():
        try:
            col1, col2, col3, col4 = st.columns(4, gap='medium')

            with col3:
                year = st.selectbox(label='Year ', options=top_sales.year())

            with col2:
                month = st.selectbox(label='Month ', options=top_sales.month(year))

            with col1:
                day = st.selectbox(label='Day ', options=top_sales.day(month, year))

            with col4:
                dept = st.selectbox(label='Dept ', options=top_sales.top_store_dept(day, month, year))

            return day, month, year, dept

        except Exception as e:
            st.error(f"Error in filter options: {e}")
            return None, None, None, None

    @staticmethod
    def top_dept_sales(condition):
        query = f"""
            SELECT dept, SUM(weekly_sales) as weekly_sales
            FROM sales
            WHERE {condition}
            GROUP BY dept
            ORDER BY weekly_sales DESC
            LIMIT 10
        """
        results = top_sales.execute_query(query)
        if results:
            index = [i for i in range(1, len(results)+1)]
            df = pd.DataFrame(results, columns=['Dept', 'Weekly Sales'], index=index)
            df['Weekly Sales'] = df['Weekly Sales'].apply(lambda x: f"{x:.2f}")
            df['dept_x'] = df['Dept'].apply(lambda x: str(x)+'*')
            return df.rename_axis('s.no')
        return pd.DataFrame()



class comparison:

    @staticmethod
    def execute_query(query, params=None):
        try:
            conn = sqlite3.connect('retail_forecast.db')
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except sqlite3.Error as e:
            st.error(f"Query error: {e}")
            return None

    @staticmethod
    def year():
        results = comparison.execute_query(
            "SELECT DISTINCT year FROM sales ORDER BY year ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def month(year):
        if year is None:
            return []
        results = comparison.execute_query(
            "SELECT DISTINCT month FROM sales WHERE year = ? ORDER BY month ASC",
            (year,)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def day(month, year):
        if month is None or year is None:
            return []
        results = comparison.execute_query(
            "SELECT DISTINCT day FROM sales WHERE year = ? AND month = ? ORDER BY day ASC",
            (year, month)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def store(day, month, year):
        if any(v is None for v in [day, month, year]):
            return []
        results = comparison.execute_query(
            """SELECT DISTINCT store FROM sales 
               WHERE day = ? AND month = ? AND year = ? 
               ORDER BY store ASC""",
            (day, month, year)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def dept(day, month, year, store):
        if any(v is None for v in [day, month, year, store]):
            return []
        results = comparison.execute_query(
            """SELECT DISTINCT dept FROM sales 
               WHERE day = ? AND month = ? AND year = ? AND store = ?
               ORDER BY dept ASC""",
            (day, month, year, store)
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def previous_week_filter_options():
        try:
            col1, col2, col3, col4, col5 = st.columns(5, gap='medium')

            with col3:
                year = st.selectbox(label='Year', options=comparison.year())

            with col2:
                month = st.selectbox(label='Month', options=comparison.month(year))

            with col1:
                day = st.selectbox(label='Day', options=comparison.day(month, year))

            with col4:
                store = st.selectbox(label='Store', options=comparison.store(day, month, year))

            with col5:
                dept = st.selectbox(label='Dept', options=comparison.dept(day, month, year, store))

            return day, month, year, store, dept
        except Exception as e:
            st.error(f"Error in filter options: {e}")
            return None, None, None, None, None

    @staticmethod
    def sql(condition):
        query = f"""
            SELECT * FROM sales 
            WHERE {condition}
            ORDER BY year, month, day, store, dept ASC
        """
        results = comparison.execute_query(query)
        if results:
            columns = ['day', 'month', 'year', 'store', 'dept', 'type', 'weekly_sales',
                      'size', 'is_holiday', 'temperature', 'fuel_price', 'markdown1',
                      'markdown2', 'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
            df = pd.DataFrame(results, columns=columns)
            return df
        return pd.DataFrame()

    @staticmethod
    def vertical_line():
        line_width = 2
        line_color = 'grey'

        # Use HTML and CSS to create the vertical line
        st.markdown(
            f"""
            <style>
                .vertical-line {{
                    border-left: {line_width}px solid {line_color};
                    height: 100vh;
                    position: absolute;
                    left: 55%;
                    margin-left: -{line_width / 2}px;
                }}
            </style>
            <div class="vertical-line"></div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def previous_week_day(month, year):
        if month is None or year is None:
            return []
        results = execute_query(
            "SELECT DISTINCT day FROM sales WHERE year = ? AND month = ? ORDER BY day ASC",
            (year, month)
        )
        if results:
            data = [i[0] for i in results]
            if month == 2 and year == 2020:
                data.remove(data[0])
            return data
        return []

    @staticmethod
    def previous_week_sales_comparison(df, day, month, year):

        index = df.index[(df['day'] == day) & (df['month'] == month) & (df['year'] == year)]
        current_index = index[0]-1
        previous_index = index[0]-2

        previous_data, current_data = {}, {}
        column_names = df.columns
        for i in range(0, len(column_names)):
            current_data[column_names[i]] = df.iloc[current_index, i]
            previous_data[column_names[i]] = df.iloc[previous_index, i]

        previous_date = f"{previous_data['day']}-{previous_data['month']}-{previous_data['year']}"

        holiday = {0: 'No', 1: 'Yes'}
        type = {1: 'A', 2: 'B', 3: 'C'}
        st.code(f'''Type : {type[current_data['type']]}        Size : {current_data['size']}        Holiday : Previous Week = {holiday[previous_data['is_holiday']]} ({previous_date}) ;     Current Week = {holiday[current_data['is_holiday']]}''')

        comparison.vertical_line()
        col1, col2 = st.columns([0.55, 0.45])

        with col1:
            for i in ['weekly_sales', 'temperature', 'fuel_price', 'cpi', 'unemployment']:
                p, c = previous_data[i], current_data[i]
                diff = ((c-p)/p)*100

                if p != 0:
                    col3, col4, col5, col6 = st.columns([0.3, 0.4, 0.25, 0.05])
                    with col3:
                        add_vertical_space(1)
                        st.markdown(f"#### {previous_data[i]:.2f}")

                    with col4:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                        No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col5:
                        add_vertical_space(1)
                        st.markdown(f"#### {current_data[i]:.2f}")

        with col2:
            for i in ['markdown1', 'markdown2', 'markdown3', 'markdown4', 'markdown5']:
                p, c = previous_data[i], current_data[i]
                diff = ((c-p)/p)*100

                if p != 0:
                    col7, col8, col9, col10 = st.columns(
                        [0.05, 0.3, 0.4, 0.25])
                    with col8:
                        add_vertical_space(1)
                        st.markdown(f"#### {previous_data[i]:.2f}")

                    with col9:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                        No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col10:
                        add_vertical_space(1)
                        st.markdown(f"#### {current_data[i]:.2f}")


    @staticmethod
    def manual_filter_options():

        col16, col17 = st.columns(2, gap='large')

        with col16:

            col6, col7, col8 = st.columns(3)

            with col8:
                year1 = st.selectbox(label='Year1', options=comparison.year())

            with col7:
                month1 = st.selectbox(
                    label='Month1', options=comparison.month(year1))

            with col6:
                day1 = st.selectbox(
                    label='Day1', options=comparison.day(month1, year1))

            col9A, col9, col10, col10A = st.columns([0.1, 0.4, 0.4, 0.1])

            with col9:
                store1 = st.selectbox(
                    label='Store1', options=comparison.store(day1, month1, year1))

            with col10:
                dept1 = st.selectbox(label='Dept1', options=comparison.dept(
                    day1, month1, year1, store1))

        with col17:

            col11, col12, col13 = st.columns(3)

            with col13:
                year2 = st.selectbox(label='Year2', options=comparison.year())

            with col12:
                month2 = st.selectbox(
                    label='Month2', options=comparison.month(year2))

            with col11:
                day2 = st.selectbox(
                    label='Day2', options=comparison.day(month2, year2))

            col14A, col14, col15, col15A = st.columns([0.1, 0.4, 0.4, 0.1])

            with col14:
                manual_store = comparison.store(day2, month2, year2)
                manual_store[0], manual_store[1] = manual_store[1], manual_store[0]
                store2 = st.selectbox(label='Store2', options=manual_store)

            with col15:
                if year1 == year2 and month1 == month2 and day1 == day2 and store1 == store2:
                    dept = comparison.dept(day2, month2, year2, store2)
                    dept.remove(dept1)
                    dept2 = st.selectbox(label='Dept2', options=dept)
                else:
                    dept2 = st.selectbox(label='Dept2', options=comparison.dept(
                        day2, month2, year2, store2))

        return day1, month1, year1, store1, dept1, day2, month2, year2, store2, dept2


    @staticmethod
    def manual_comparison(df1, df2):

        data1 = df1.iloc[0, :]
        df1_dict = data1.to_dict()

        data2 = df2.iloc[0, :]
        df2_dict = data2.to_dict()

        col1, col2, col3 = st.columns([0.1, 0.9, 0.1])
        with col2:
            holiday = {0: 'No', 1: 'Yes'}
            type = {1: 'A', 2: 'B', 3: 'C'}
            st.code(f'''{type[df1_dict['type']]} : Type : {type[df2_dict['type']]}           {df1_dict['size']} : Size : {df2_dict['size']}           {holiday[df1_dict['is_holiday']]}  :  Holiday : {holiday[df2_dict['is_holiday']]}''')

        comparison.vertical_line()
        col1, col2 = st.columns([0.55, 0.45])

        with col1:

            for i in ['weekly_sales', 'temperature', 'fuel_price', 'cpi', 'unemployment']:
                p, c = df1_dict[i], df2_dict[i]
                diff = ((c-p)/p)*100

                if p != 0:
                    col3, col4, col5, col6 = st.columns([0.3, 0.4, 0.25, 0.05])
                    with col3:
                        add_vertical_space(1)
                        st.markdown(f"#### {df1_dict[i]:.2f}")

                    with col4:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                        No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col5:
                        add_vertical_space(1)
                        st.markdown(f"#### {df2_dict[i]:.2f}")

        with col2:

            for i in ['markdown1', 'markdown2', 'markdown3', 'markdown4', 'markdown5']:
                p, c = df1_dict[i], df2_dict[i]
                diff = ((c-p)/p)*100

                if p != 0:
                    col7, col8, col9, col10 = st.columns(
                        [0.05, 0.3, 0.4, 0.25])
                    with col8:
                        add_vertical_space(1)
                        st.markdown(f"#### {df1_dict[i]:.2f}")

                    with col9:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                        No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col10:
                        add_vertical_space(1)
                        st.markdown(f"#### {df2_dict[i]:.2f}")


    @staticmethod
    def top_store_filter_options():

        col1, col2, col3, col4 = st.columns(4, gap='medium')

        with col3:
            year = st.selectbox(label='Year ', options=comparison.year())

        with col2:
            month = st.selectbox(
                label='Month ', options=comparison.month(year))

        with col1:
            day = st.selectbox(
                label='Day ', options=comparison.day(month, year))

        with col4:
            store = st.selectbox(
                label='Store ', options=comparison.store(day, month, year))

        return day, month, year, store


    @staticmethod
    def top_store_sales(condition):

        gopi = sqlite3.connect('retail_forecast.db')
        cursor = gopi.cursor()

        cursor.execute(f'''select distinct store, type, sum(weekly_sales) as weekly_sales,  
                        size, is_holiday, avg(temperature) as temperature,  
                        avg(fuel_price) as fuel_price, avg(markdown1) as markdown1,  
                        avg(markdown2) as markdown2, avg(markdown3) as markdown3,  
                        avg(markdown4) as markdown4, avg(markdown5) as markdown5, 
                        avg(cpi) as cpi, avg(unemployment) as unemployment
                       
                        from sales
                        where {condition}
                        group by store, type, size, is_holiday               
                        order by weekly_sales desc;''')

        s = cursor.fetchall()

        index = [i for i in range(1, len(s)+1)]
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(s, columns=columns, index=index)
        df['weekly_sales'] = df['weekly_sales'].apply(lambda x: f'{x:.2f}')
        df = df.rename_axis('s.no')

        cursor.close()
        gopi.close()
        return df


    @staticmethod
    def compare_store(df1, df2, i):

        data1 = df1.iloc[i, :]
        df1_dict = data1.to_dict()

        data2 = df2.iloc[0, :]
        df2_dict = data2.to_dict()

        holiday = {0: 'No', 1: 'Yes'}
        type = {1: 'A', 2: 'B', 3: 'C'}
        st.code(f'''{df1_dict['store']} : Store : {df2_dict['store']}           {type[df1_dict['type']]} : Type : {type[df2_dict['type']]}           {df1_dict['size']} : Size : {df2_dict['size']}           {holiday[df1_dict['is_holiday']]}  :  Holiday : {holiday[df2_dict['is_holiday']]}''')

        comparison.vertical_line()
        col1, col2 = st.columns([0.55, 0.45])

        with col1:

            for i in ['weekly_sales', 'temperature', 'fuel_price', 'cpi', 'unemployment']:
                p, c = float(df1_dict[i]), float(df2_dict[i])

                if p != 0:
                    diff = ((c-p)/p)*100
                    col3, col4, col5, col6 = st.columns([0.3, 0.4, 0.25, 0.05])
                    with col3:
                        add_vertical_space(1)
                        st.markdown(f"#### {float(df1_dict[i]):.2f}")

                    with col4:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                                    No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col5:
                        add_vertical_space(1)
                        st.markdown(f"#### {float(df2_dict[i]):.2f}")

                else:
                    col3, col4, col5, col6 = st.columns([0.3, 0.4, 0.25, 0.05])
                    with col3:
                        add_vertical_space(1)
                        st.markdown(f"#### {df1_dict[i]:.2f}")

                    with col4:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                                    No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{c*100:.2f}%")

                    with col5:
                        add_vertical_space(1)
                        st.markdown(f"#### {df2_dict[i]:.2f}")

        with col2:

            for i in ['markdown1', 'markdown2', 'markdown3', 'markdown4', 'markdown5']:
                p, c = df1_dict[i], df2_dict[i]
                diff = ((c-p)/p)*100

                if p != 0:
                    col7, col8, col9, col10 = st.columns(
                        [0.05, 0.3, 0.4, 0.25])
                    with col8:
                        add_vertical_space(1)
                        st.markdown(f"#### {df1_dict[i]:.2f}")

                    with col9:
                        if f"{c:.2f}" == f"{p:.2f}":
                            add_vertical_space(1)
                            st.markdown(f'''<h5 style="text-align: left;">{columns_dict()[i]} <br>
                                                    No Impact</h5>''', unsafe_allow_html=True)
                            add_vertical_space(2)
                        else:
                            st.metric(
                                label=columns_dict()[i], value=f"{(c-p):.2f}", delta=f"{diff:.2f}%")

                    with col10:
                        add_vertical_space(1)
                        st.markdown(f"#### {df2_dict[i]:.2f}")

        add_vertical_space(3)


    @staticmethod
    def compare_with_top_stores(df1, df2):

        store_list = df1['store'].tolist()

        user_store = df2['store'].tolist()[0]

        if user_store in store_list:

            if store_list[0] == user_store:
                col1, col2, col3 = st.columns([0.29, 0.42, 0.29])
                with col2:
                    st.info('The Selected Store Ranks Highest in Weekly Sales')
            
            else:
                user_store_index = store_list.index(user_store)
                for i in range(0, user_store_index):
                    comparison.compare_store(df1,df2,i)

        else:

            for i in range(1, 10):
                comparison.compare_store(df1,df2,i)


    @staticmethod
    def compare_with_bottom_stores(df1, df2):
        """
        Compare user selected store with bottom 10 stores
        df1: DataFrame containing bottom 10 stores
        df2: DataFrame containing user selected store
        """
        store_list = df1['store'].tolist()
        user_store = df2['store'].tolist()[0]

        if user_store in store_list:
            if store_list[-1] == user_store:
                col1, col2, col3 = st.columns([0.30, 0.40, 0.30])
                with col2:
                    st.info('The Selected Store Ranks Lowest in Weekly Sales')
            else:
                user_store_index = store_list.index(user_store)
                for i in range(user_store_index+1, len(store_list)):
                    comparison.compare_store(df1, df2, i)
        else:
            for i in range(len(store_list)-10, len(store_list)):
                comparison.compare_store(df1, df2, i)

    @staticmethod
    def bottom_store_sales(condition):
        """
        Get store sales data ordered by weekly sales ascending
        """
        query = f"""
            SELECT DISTINCT store, type, SUM(weekly_sales) as weekly_sales,  
            size, is_holiday, AVG(temperature) as temperature,  
            AVG(fuel_price) as fuel_price, AVG(markdown1) as markdown1,  
            AVG(markdown2) as markdown2, AVG(markdown3) as markdown3,  
            AVG(markdown4) as markdown4, AVG(markdown5) as markdown5, 
            AVG(cpi) as cpi, AVG(unemployment) as unemployment
            FROM sales
            WHERE {condition}
            GROUP BY store, type, size, is_holiday               
            ORDER BY weekly_sales ASC
        """
        results = comparison.execute_query(query)
        if results:
            index = [i for i in range(1, len(results)+1)]
            columns = ['store', 'type', 'weekly_sales', 'size', 'is_holiday', 
                      'temperature', 'fuel_price', 'markdown1', 'markdown2', 
                      'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
            df = pd.DataFrame(results, columns=columns, index=index)
            df['weekly_sales'] = df['weekly_sales'].apply(lambda x: f'{x:.2f}')
            return df.rename_axis('s.no')
        return pd.DataFrame()

    @staticmethod
    def bottom_store_filter_options():
        """
        Filter options for bottom stores comparison
        """
        try:
            col1, col2, col3, col4 = st.columns(4, gap='medium')

            with col3:
                year = st.selectbox(label='Year  ', options=comparison.year())

            with col2:
                month = st.selectbox(label='Month  ', options=comparison.month(year))

            with col1:
                day = st.selectbox(label='Day  ', options=comparison.day(month, year))

            with col4:
                store = st.selectbox(label='Store  ', options=comparison.store(day, month, year))

            return day, month, year, store

        except Exception as e:
            st.error(f"Error in bottom store filter options: {e}")
            return None, None, None, None



class features:

    @staticmethod
    def get_db_connection():
        try:
            conn = sqlite3.connect('retail_forecast.db')
            conn.row_factory = sqlite3.Row  # This enables column access by name
            return conn
        except sqlite3.Error as e:
            st.error(f"Database connection error: {e}")
            return None

    @staticmethod
    def execute_query(query):
        conn = features.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
            except sqlite3.Error as e:
                st.error(f"Query error: {e}")
                return None

    @staticmethod
    def month(year):
        if year is None:
            return []
        results = features.execute_query(
            f"SELECT DISTINCT month FROM sales WHERE year={year} ORDER BY month ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def year():
        """Get distinct years from sales table"""
        results = features.execute_query(
            "SELECT DISTINCT year FROM sales ORDER BY year ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def day(month, year):
        """Get distinct days based on month and year"""
        if month is None or year is None:
            return []
        results = features.execute_query(
            f"SELECT DISTINCT day FROM sales WHERE month={month} AND year={year} ORDER BY day ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def filter_options():
        """Filter options for features date section"""
        try:
            col1, col2, col3 = st.columns(3, gap='medium')

            with col3:
                years = features.year()
                if not years:
                    st.error("No years found in database")
                    return None, None, None
                year = st.selectbox('Year', options=years)

            with col2:
                months = features.month(year)
                if not months:
                    st.error("No months found for selected year")
                    return None, None, None
                month = st.selectbox('Month', options=months)

            with col1:
                days = features.day(month, year)
                if not days:
                    st.error("No days found for selected month and year")
                    return None, None, None
                day = st.selectbox('Day', options=days)

            return day, month, year
        except Exception as e:
            st.error(f"Error in filter options: {e}")
            return None, None, None

    @staticmethod
    def sql_sum_avg(condition, params=None):
        query = f"""
            SELECT DISTINCT store, type, SUM(weekly_sales) as weekly_sales,  
            size, is_holiday, AVG(temperature) as temperature,  
            AVG(fuel_price) as fuel_price, AVG(markdown1) as markdown1,  
            AVG(markdown2) as markdown2, AVG(markdown3) as markdown3,  
            AVG(markdown4) as markdown4, AVG(markdown5) as markdown5, 
            AVG(cpi) as cpi, AVG(unemployment) as unemployment
            FROM sales
            WHERE {condition}
            GROUP BY store, type, size, is_holiday               
            ORDER BY weekly_sales DESC
        """
        results = execute_query(query, params)
        if results:
            columns = ['store', 'type', 'weekly_sales', 'size', 'is_holiday', 
                      'temperature', 'fuel_price', 'markdown1', 'markdown2', 
                      'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
            return pd.DataFrame(results, columns=columns)
        return pd.DataFrame()

    @staticmethod
    def store():
        results = features.execute_query(
            "SELECT DISTINCT store FROM sales ORDER BY store ASC"
        )
        if results:
            return [i[0] for i in results]
        return []

    @staticmethod
    def sql(condition):
        results = features.execute_query(f"""
            SELECT * FROM sales WHERE {condition}
            ORDER BY year, month, day, store, dept ASC
        """)
        
        if results:
            index = [i for i in range(1, len(results)+1)]
            columns = ['day', 'month', 'year', 'store', 'dept', 'type', 'weekly_sales',
                      'size', 'is_holiday', 'temperature', 'fuel_price', 'markdown1',
                      'markdown2', 'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
            df = pd.DataFrame(results, columns=columns, index=index)
            return df.rename_axis('s.no')
        return pd.DataFrame()

    @staticmethod
    def sql_holiday(condition):
        results = features.execute_query(f"""
            SELECT is_holiday, AVG(weekly_sales) as weekly_sales
            FROM sales
            WHERE {condition}
            GROUP BY is_holiday
        """)
        
        if results:
            index = [i for i in range(1, len(results)+1)]
            df = pd.DataFrame(results, columns=['is_holiday', 'weekly_sales'], index=index)
            df['weekly_sales'] = df['weekly_sales'].apply(lambda x: f"{x:.2f}")
            df['decode'] = df['is_holiday'].apply(lambda x: 'Yes' if x==1 else 'No')
            df.drop(columns=['is_holiday'], inplace=True)
            return df.rename_axis('s.no')
        return pd.DataFrame()

    @staticmethod
    def store_features(df):
        columns = ['temperature', 'fuel_price', 'markdown1', 'markdown2',
                  'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
        
        color = ['#5D9A96','#5cb85c','#5D9A96','#5cb85c',
                 '#5D9A96','#5cb85c','#5D9A96','#5cb85c','#5D9A96']
        
        c = 0
        for i in columns:
            # create 10 bins based on range values [like 20-40, 40-60, etc.,]
            df1 = features.bins(df=df, feature=i)

            # group unique values and sum weekly_sales
            df2 = df1.groupby('part')['weekly_sales'].sum().reset_index()

            # only select weekly sales greater than zero
            df2 = df2[df2['weekly_sales']>0]

            # barchart with df2 dataframe values
            plotly.vertical_bar_chart(df=df2, x='part', y='weekly_sales',
                                    color=color[c], text='part',
                                    title_x=0.40, title=columns_dict()[i])
            
            c += 1
            add_vertical_space(2)

    @staticmethod
    def bins(df, feature):
        # filter 2 columns
        df1 = df[['weekly_sales',feature]]

        # Calculate bin edges
        bin_edges = pd.cut(df1[feature], bins=10, labels=False, retbins=True)[1]

        # Create labels for the bins
        bin_labels = [f'{f"{bin_edges[i]:.2f}"} to <br>{f"{bin_edges[i+1]:.2f}"}' 
                     for i in range(0, len(bin_edges)-1)]

        # Create a new column by splitting into 10 bins
        df1['part'] = pd.cut(df1[feature], bins=bin_edges, labels=bin_labels, include_lowest=True)

        return df1



class prediction:

    @staticmethod
    def type_size_dict():
        try:
            conn = get_db_connection()
            if not conn:
                return {}, {}
                
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT store, type, size 
                FROM sales
                GROUP BY store, type, size
                ORDER BY store ASC
            """)
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            type_dict = {row[0]: row[1] for row in results}
            size_dict = {row[0]: row[2] for row in results}
            
            return type_dict, size_dict
        except Exception as e:
            st.error(f"Error getting type and size data: {e}")
            return {}, {}

    @staticmethod
    def get_feature_ranges():
        try:
            conn = get_db_connection()
            if not conn:
                return {}
                
            cursor = conn.cursor()
            
            # Get min/max values for numerical features
            features = ['temperature', 'fuel_price', 'markdown1', 'markdown2', 
                       'markdown3', 'markdown4', 'markdown5', 'cpi', 'unemployment']
            
            ranges = {}
            for feature in features:
                cursor.execute(f"SELECT MIN({feature}), MAX({feature}) FROM sales")
                min_val, max_val = cursor.fetchone()
                ranges[feature] = {'min': min_val, 'max': max_val}
            
            cursor.close()
            conn.close()
            return ranges
        except Exception as e:
            st.error(f"Error getting feature ranges: {e}")
            return {}

    @staticmethod
    def dept(store):
        try:
            conn = get_db_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT dept 
                FROM sales
                WHERE store = ?
                ORDER BY dept ASC
            """, (store,))
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [row[0] for row in results]
        except Exception as e:
            st.error(f"Error getting departments: {e}")
            return []

    @staticmethod
    def validate_input(value, feature_name, ranges):
        """Validate input values against allowed ranges"""
        if feature_name in ranges:
            min_val = ranges[feature_name]['min']
            max_val = ranges[feature_name]['max']
            if value < min_val or value > max_val:
                st.warning(f"{feature_name} should be between {min_val:.2f} and {max_val:.2f}")
                return False
        return True

    @staticmethod
    def predict_weekly_sales():
        try:
            # Get feature ranges for validation
            feature_ranges = prediction.get_feature_ranges()
            
            # Get input from users
            with st.form('prediction'):
                col1, col2, col3 = st.columns([0.5, 0.1, 0.5])

                with col1:
                    user_date = st.date_input(
                        label='Date', 
                        min_value=date(2020, 2, 5),
                        max_value=date(2023, 12, 31), 
                        value=date(2020, 2, 5)
                    )

                    store = st.number_input(
                        label='Store', 
                        min_value=1, 
                        max_value=45,
                        value=1, 
                        step=1
                    )

                    dept = st.selectbox(
                        label='Department',
                        options=prediction.dept(store)
                    )

                    holiday = st.selectbox(
                        label='Holiday', 
                        options=['No', 'Yes']
                    )

                    temperature = st.number_input(
                        label='Temperature(°F)',
                        value=feature_ranges.get('temperature', {}).get('min', 0.0),
                        min_value=feature_ranges.get('temperature', {}).get('min', -10.0),
                        max_value=feature_ranges.get('temperature', {}).get('max', 110.0)
                    )

                    fuel_price = st.number_input(
                        label='Fuel Price',
                        value=feature_ranges.get('fuel_price', {}).get('min', 2.47),
                        min_value=0.0,
                        max_value=feature_ranges.get('fuel_price', {}).get('max', 10.0)
                    )

                with col3:
                    markdown1 = st.number_input(
                        label='MarkDown1',
                        value=feature_ranges.get('markdown1', {}).get('min', 0.0)
                    )

                    markdown2 = st.number_input(
                        label='MarkDown2',
                        value=feature_ranges.get('markdown2', {}).get('min', 0.0)
                    )

                    markdown3 = st.number_input(
                        label='MarkDown3',
                        value=feature_ranges.get('markdown3', {}).get('min', 0.0)
                    )

                    markdown4 = st.number_input(
                        label='MarkDown4',
                        value=feature_ranges.get('markdown4', {}).get('min', 0.0)
                    )

                    markdown5 = st.number_input(
                        label='MarkDown5',
                        value=feature_ranges.get('markdown5', {}).get('min', 0.0)
                    )

                    cpi = st.number_input(
                        label='CPI',
                        value=feature_ranges.get('cpi', {}).get('min', 126.06),
                        min_value=feature_ranges.get('cpi', {}).get('min', 100.0),
                        max_value=feature_ranges.get('cpi', {}).get('max', 250.0)
                    )

                    unemployment = st.number_input(
                        label='Unemployment',
                        value=feature_ranges.get('unemployment', {}).get('min', 3.68),
                        min_value=0.0,
                        max_value=feature_ranges.get('unemployment', {}).get('max', 20.0)
                    )

                    add_vertical_space(2)
                    button = st.form_submit_button(label='PREDICT')
                    style_submit_button()

            # Validate and predict when button is clicked
            if button:
                # Validate inputs
                features_to_validate = {
                    'temperature': temperature,
                    'fuel_price': fuel_price,
                    'markdown1': markdown1,
                    'markdown2': markdown2,
                    'markdown3': markdown3,
                    'markdown4': markdown4,
                    'markdown5': markdown5,
                    'cpi': cpi,
                    'unemployment': unemployment
                }

                # Validate all inputs
                valid = all(prediction.validate_input(value, name, feature_ranges) 
                          for name, value in features_to_validate.items())

                if valid:
                    with st.spinner('Predicting sales...'):
                        # Load the model
                        try:
                            with open('model1_markdown.pkl', 'rb') as f:
                                model = pickle.load(f)
                        except Exception as e:
                            st.error(f"Error loading model: {e}")
                            return None

                        # Get store type and size
                        type_dict, size_dict = prediction.type_size_dict()
                        holiday_dict = {'Yes': 1, 'No': 0}

                        # Prepare input data
                        user_data = np.array([[
                            user_date.day, user_date.month, user_date.year,
                            store, dept, type_dict.get(store, 1), size_dict.get(store, 0),
                            holiday_dict[holiday], temperature,
                            fuel_price, markdown1, markdown2, markdown3,
                            markdown4, markdown5, cpi, unemployment
                        ]])

                        # Make prediction
                        try:
                            y_pred = model.predict(user_data)[0]
                            return f"{max(0, y_pred):.2f}"  # Ensure non-negative prediction
                        except Exception as e:
                            st.error(f"Error making prediction: {e}")
                            return None

        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None


# Database helper functions
def get_db_connection():
    try:
        conn = sqlite3.connect('retail_forecast.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def execute_query(query, params=None):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except sqlite3.Error as e:
            st.error(f"Query error: {e}")
            return None

def check_database():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sales")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return count > 0
    except:
        return False

def initialize_database():
    if not check_database():
        try:
            # Check if dataset exists
            if not os.path.exists('dataset/df_sql.csv'):
                st.error("Dataset file not found. Please place df_sql.csv in the dataset folder.")
                return False
                
            # Create table
            sql.create_table()
            
            # Load dataset
            df = pd.read_csv('dataset/df_sql.csv')
            
            # Data migration
            sql.data_migration()
            
            st.success("Database initialized successfully!")
            return True
        except Exception as e:
            st.error(f"Error initializing database: {e}")
            return False
    return True

def ensure_directories():
    try:
        # Create dataset directory if it doesn't exist
        os.makedirs('dataset', exist_ok=True)
        
        # Check if dataset file exists
        if not os.path.exists('dataset/df_sql.csv'):
            st.error("""
                Dataset file not found. Please:
                1. Create a 'dataset' folder in the application directory
                2. Place df_sql.csv in the dataset folder
            """)
            return False
        return True
    except Exception as e:
        st.error(f"Error creating directories: {e}")
        return False

streamlit_config()

# Ensure directories and dataset exist
if not ensure_directories():
    st.stop()

# Initialize database before showing the menu
if not initialize_database():
    st.error("Please make sure the dataset file 'dataset/df_sql.csv' exists")
    st.stop()

with st.sidebar:
    add_vertical_space(1)
    option = option_menu(
        menu_title='', 
        options=['Top Sales', 'Comparison', 'Features', 'Prediction', 'Exit'],
        icons=['database-fill', 'bar-chart-line', 'globe', 'list-task', 'slash-square', 'sign-turn-right-fill']
    )
    
    col1, col2, col3 = st.columns([0.26, 0.48, 0.26])
    with col2:
        button = st.button(label='Submit')



if button and option == 'Migrating to SQL':

    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])

    with col2:

        add_vertical_space(2)

        with st.spinner('Dropping the Existing Table...'):
            sql.drop_table()
        
        with st.spinner('Creating Sales Table...'):
            sql.create_table()
        
        with st.spinner('Migrating Data to SQL Database...'):
            sql.data_migration()

        st.success('Successfully Data Migrated to SQL Database')
        st.balloons()



elif option == 'Top Sales':
    tab1, tab2 = st.tabs(['Top Stores', 'Top Product Category'])

    with tab1:
        day1, month1, year1, dept1 = top_sales.top_store_filter_options()
        if all(v is not None for v in [day1, month1, year1]):
            add_vertical_space(3)

            if dept1 == 'Overall':
                df1 = top_sales.top_store_sales(
                    f"day={day1} AND month={month1} AND year={year1}")
            else:
                df1 = top_sales.top_store_sales(
                    f"day={day1} AND month={month1} AND year={year1} AND dept={dept1}")

            if not df1.empty:
                plotly.vertical_bar_chart(df=df1, x='store_x', y='Weekly Sales', 
                                        text='Weekly Sales', color='#5D9A96', 
                                        title='Top Stores in Weekly Sales', title_x=0.35)
            else:
                st.warning("No data available for the selected filters")

    with tab2:
        day2, month2, year2, store2 = top_sales.top_dept_filter_options()
        if all(v is not None for v in [day2, month2, year2]):
            add_vertical_space(3)

            if store2 == 'Overall':
                df2 = top_sales.top_dept_sales(
                    f"day={day2} AND month={month2} AND year={year2}")
            else:
                df2 = top_sales.top_dept_sales(
                    f"day={day2} AND month={month2} AND year={year2} AND store={store2}")

            if not df2.empty:
                plotly.vertical_bar_chart(df=df2, x='dept_x', y='Weekly Sales',
                                        text='Weekly Sales', color='#5cb85c',
                                        title='Top Product Category in Weekly Sales Of Each Store', title_x=0.35)
            else:
                st.warning("No data available for the selected filters")



elif option == 'Comparison':

    tab1, tab2, tab3, tab4 = st.tabs(['Previous Week', 'Top Stores', 
                                      'Bottom Stores','Manual Comparison'])

    with tab1:

        day, month, year, store, dept = comparison.previous_week_filter_options()
        add_vertical_space(3)

        df = comparison.sql(f"store='{store}' and dept='{dept}'")

        comparison.previous_week_sales_comparison(df, day, month, year)


    with tab2:

        # user input filter options
        day3, month3, year3, store3 = comparison.top_store_filter_options()
        add_vertical_space(3)

        # sql query filter the data based on user input day,month,year, store
        df3 = comparison.top_store_sales(f"""day='{day3}' and month='{month3}' and 
                                 year='{year3}' and store='{store3}'""")

        # sql query calculte the sum of weekly sales in desc order (1 to 45) all stores
        df4 = comparison.top_store_sales(f"""day='{day3}' and month='{month3}' and 
                                 year='{year3}'""")

        # top 10 stores in weekly sales
        df_top10 = df4.iloc[:10, :]

        # user selected store compare to top 10 stores based on weekly sales
        comparison.compare_with_top_stores(df_top10, df3)


    with tab3:
        # user input filter options
        day4, month4, year4, store4 = comparison.bottom_store_filter_options()
        
        if all(v is not None for v in [day4, month4, year4, store4]):
            add_vertical_space(3)

            # sql query filter the data based on user input day,month,year, store
            df5 = comparison.bottom_store_sales(
                f"day={day4} AND month={month4} AND year={year4} AND store={store4}"
            )

            # sql query calculate the sum of weekly sales in asc order
            df6 = comparison.bottom_store_sales(
                f"day={day4} AND month={month4} AND year={year4}"
            )

            if not df6.empty:
                # bottom 10 stores in weekly sales
                df_bottom10 = df6.iloc[-10:, :]

                # user selected store compare to bottom 10 stores based on weekly sales
                comparison.compare_with_bottom_stores(df_bottom10, df5)
            else:
                st.warning("No data available for the selected filters")


    with tab4:

        day1, month1, year1, store1, dept1, day2, month2, year2, store2, dept2 = comparison.manual_filter_options()
        add_vertical_space(3)

        df1 = comparison.sql(f"""day='{day1}' and month='{month1}' and year='{year1}' and 
                                 store='{store1}' and dept='{dept1}'""")

        df2 = comparison.sql(f"""day='{day2}' and month='{month2}' and year='{year2}' and 
                                 store='{store2}' and dept='{dept2}'""")

        comparison.manual_comparison(df1, df2)



elif option == 'Features':

    tab1, tab2 = st.tabs(['Date', 'Store'])
    
    with tab1:
        day, month, year = features.filter_options()
        
        if all(v is not None for v in [day, month, year]):
            # sum of weekly sales and avg of remaining values from sales table
            df = features.sql_sum_avg(f"day={day} AND month={month} AND year={year}")
            add_vertical_space(2)

            if not df.empty:
                columns = ['size', 'type', 'temperature', 'fuel_price', 'markdown1', 
                          'markdown2', 'markdown3', 'markdown4', 'markdown5', 'cpi', 
                          'unemployment']
                
                for i in columns:
                    plotly.scatter_chart(df=df, x=i, y='weekly_sales')
            else:
                st.warning("No data available for the selected filters")
        else:
            st.warning("Please select valid date filters")

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            store = st.selectbox(label='Store', options=features.store())
        
        if store is not None:
            add_vertical_space(2)
            df = features.sql(f'store={store}')
            holiday_df = features.sql_holiday(f'store={store}')

            if not holiday_df.empty:
                plotly.pie_chart(df=holiday_df, x='decode', y='weekly_sales',
                               title='Holiday', title_x=0.40)

            if not df.empty:
                features.store_features(df)
            else:
                st.warning("No data available for the selected store")



elif option == 'Prediction':

    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None

    # Make prediction
    prediction_result = prediction.predict_weekly_sales()
    
    if prediction_result:
        style_prediction()
        st.markdown(
            f'### <div class="center-text">Predicted Weekly Sales: ₹{prediction_result}</div>',
            unsafe_allow_html=True
        )
        
        # Show success animation
        st.balloons()
        
        # Add some context
        st.info("""
        This prediction is based on historical sales data and the provided features.
        Actual results may vary based on additional factors not captured in the model.
        """)



elif option == 'Exit':
    
    add_vertical_space(2)

    col1,col2,col3 = st.columns([0.20,0.60,0.20])

    with col2:

        st.success('#### Thank you for your time. Exiting the application')
        st.balloons()

# 