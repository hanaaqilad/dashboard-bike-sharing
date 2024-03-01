import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
# sns.set(style='dark')

# path_labels = os.getcwd() + 'main/dashboard/all_df.csv'
all_df = pd.read_csv('/main/dashboard/all_df.csv')

all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df['dteday'] = all_df['dteday'].dt.date

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
st.title('Proyek Final Analisis Data :sparkles:')
st.text('created by - Hana')

with st.sidebar:
    st.title(":bike: :bike: :bike: :bike: :bike: :bike:")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

### LABELLING ###
labels = ['season', 'weathersit', 'weekday', 'workingday', 'holiday']
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weathersit_labels = {1: 'Clear/Few clouds', 2: 'Mist/Cloudy', 3: 'Light Precip', 4: 'Heavy Precip'}
weekday_labels = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 0: 'Sun'}
workingday_labels = {0: 'Day Off', 1: 'Working day'}
holiday_labels = {0: 'Non holiday', 1: 'Holiday'}
mnth_labels = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


### FUNCTION ###
def show_plot(param, plot):
    res_df = main_df.groupby(by=param)['cnt'].mean().reset_index()

    if param in labels:
        label = globals()[param + "_labels"]
        res_df[param] = res_df[param].map(label)

    fig, ax = plt.subplots(figsize=(20, 10))
    colors = "#49a3ba"

    if plot == "bar": 
        sns.barplot(y="cnt", x=param, data=res_df, ax=ax)
    elif plot == "line":
        sns.lineplot(y="cnt", x=param, data=res_df, ax=ax)
    elif plot == "scatter":
        sns.scatterplot(y="cnt", x=param, data=res_df, ax=ax)

    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.subheader('')

### STREAMLIT LAYOUT ###
st.header(':bike: Bike Sharing Analysis :bike:')

col1, col2 = st.columns(2)
with col1:
    total = main_df['cnt'].sum()
    total = "{:,.0f}".format(total)
    st.metric("Total Rental Sepeda", value=total)

with col2:
    average = main_df['cnt'].mean()
    st.metric("Rata-Rata Rental Sepeda", value=round(average, 2))

st.subheader('')

st.subheader('Pengaruh kondisi cuaca terhadap tingkat rental sepeda')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Kondisi Cuaca')
show_plot('weathersit','bar')

st.subheader('Tingkat rental sepeda terhadap tingginya suhu')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Suhu (normalized celcius)')
show_plot('temp','scatter')

st.subheader('Perbandingan tingkat rental sepeda terhadap musim')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Musim')
show_plot('season','bar')

st.subheader('Tingkat rental sepeda per bulannya')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Bulan')
show_plot('mnth','line')

st.subheader('Perbandingan rental sepeda antara hari kerja dan hari libur')
st.markdown('Rata-Rata Rental Sepeda saat Hari Kerja vs Hari Libur')
show_plot('workingday','bar')

st.subheader('Tingkat rental sepeda per hari')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Hari')
show_plot('weekday','bar')

st.subheader('Tingkat rental sepeda per jam')
st.markdown('Rata-Rata Rental Sepeda Berdasarkan Jam (00.00 - 23.00)')
show_plot('hr','line')
