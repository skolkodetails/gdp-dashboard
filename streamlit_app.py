import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "titanic dashboard", page_icon = "🚢oops", layout = "wide")
st.title("🚢 dashboard: titanic passengers")
st.markdown("This dashboard is created for interactive analysis of data about the passengers of the legendary Titanic \n Here we can see statistics, passenger distribution, and factors that influenced survival")
@st.cache_data #используем кэш для быстрой работы приложения
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    return pd.read_csv(url)
df = load_data()
st.divider() #горизонтальная линия
# вывод энного количества строк
st.header("1. Viewing raw data")
n_rows = st.slider("Select the number of lines to display:", min_value = 1, max_value = len(df), value = 5)
st.dataframe(df.head(n_rows))
st.divider()
# описательная статистика 
st.header("2. Descriptive statistics")
st.markdown("This section provides basic information about the format of our table and the types of data")
# разбиваем экран на 2 колонки для вывода метрик
col1, col2 = st.columns(2)
with col1:
    st.metric("Number of passengers (rows)", df.shape[0])
with col2:
    st.metric("Number of features (columns)", df.shape[1])
# вывод типов данных и названий столбцов
st.subheader("Columns and data types:")
# Преобразуем dtypes в красивую табличку
dtypes_df = pd.DataFrame(df.dtypes, columns = ['Тип данных']).astype(str)
st.dataframe(dtypes_df, use_container_width = True)
st.divider()
st.header("3. Data visualization")
# создаем две колонки чтобы разместить графики рядом
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    # Pie Chart
    st.subheader("Survival status")
    # заменим 0 и 1 на текст для понятности
    surv_counts = df['Survived'].map({0: 'dead', 1: 'survived'}).value_counts().reset_index()
    surv_counts.columns = ['status', 'amount']
    fig1 = px.pie(surv_counts, names = 'status', values = 'amount', color = 'status', 
                  color_discrete_map = {'dead': '#EF553B', 'survived': '#00CC96'})
    st.plotly_chart(fig1, use_container_width=True)
    # Bar Chart
    st.subheader("Passengers by ticket class")
    pclass_counts = df['Pclass'].value_counts().reset_index()
    pclass_counts.columns = ['Class (1-elite, 3-economy)', 'amount']
    # Делаем класс строкой, чтобы он не воспринимался как непрерывное число на графике
    pclass_counts['Class (1-elite, 3-economy)', 'Quantity'] = pclass_counts['Class (1-elite, 3-economy)'].astype(str)
    fig2 = px.bar(pclass_counts, x = 'Class (1-elite, 3-economy)', y = 'amount', color = 'Class (1-elite, 3-economy)')
    st.plotly_chart(fig2, use_container_width=True)
with chart_col2:
    # Histogram
    st.subheader("Age distribution")
    fig3 = px.histogram(df, x = "Age", nbins=20, labels={"Age": "age"}, color_discrete_sequence = ['#636EFA'])
    st.plotly_chart(fig3, use_container_width = True)
    #Scatter Plot
    st.subheader("Dependence: Age and Ticket Price")
    df_scatter = df.copy()
    df_scatter['status'] = df_scatter['Survived'].map({0: 'died', 1: 'survived'})
    fig4 = px.scatter(df_scatter, x = "Age", y = "Fare", color = "status", 
                      labels = {"Age": "age", "Fare": "price"})
    st.plotly_chart(fig4, use_container_width = True)
st.divider() 
# график реагирующий на ввод пользователя
st.header("4. Interactive survival analysis")
st.markdown("Select a parameter from the drop-down list below to see what percentage of passengers survived based on the selected feature")
selected_column = st.selectbox(
    "Select a parameter:",
    ("Sex", "Pclass", "Embarked"))
column_names = {"Sex": "Sex", "Pclass": "Pclass", "Embarked": "Embarked"}
survival_rates = df.groupby(selected_column)['Survived'].mean().reset_index()
survival_rates['Survived'] = survival_rates['Survived'] * 100 
# интерактивный столбчатый график
st.subheader(f"Percentage of survivors based on: {column_names[selected_column]}")
fig5 = px.bar(survival_rates, x=selected_column, y='Survived',
              labels = {selected_column: column_names[selected_column], 'Survived' : 'survived %'},
              color = selected_column, text_auto = '.1f') #цифры на столбики
st.plotly_chart(fig5, use_container_width = True)
