import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
import os
import numpy as np

# script_dir = os.path.dirname(os.path.realpath(__file__))
day_df = pd.read_csv("day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

st.sidebar.header("Select Date Range")
min_date = date(2011, 1, 1)
max_date = date(2012, 12, 31)
default_start_date = date(2011, 1, 1)
default_end_date = date(2011, 12, 31)
start_date = st.sidebar.date_input("Start Date", value=default_start_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=default_end_date, min_value=min_date, max_value=max_date)
filtered_df = day_df[(day_df['dteday'].dt.date >= start_date) & (day_df['dteday'].dt.date <= end_date)]

avg_usage_by_month = filtered_df.groupby('mnth')[['casual', 'registered']].mean()
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(avg_usage_by_month.index, avg_usage_by_month['casual'], label='Casual Users', marker='o')
ax1.plot(avg_usage_by_month.index, avg_usage_by_month['registered'], label='Registered Users', marker='o')
ax1.set_title('Average Bike Usage by Month (Casual vs Registered Users)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Average Number of Users')
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax1.legend()
ax1.grid(True)

avg_usage_by_holiday = filtered_df.groupby('holiday')[['casual', 'registered']].mean().reset_index()
avg_usage_by_holiday['holiday'] = avg_usage_by_holiday['holiday'].map({0: 'Workday', 1: 'Holiday'})
avg_usage_by_holiday_melted = avg_usage_by_holiday.melt(id_vars='holiday', value_vars=['casual', 'registered'], var_name='User Type', value_name='Average Users')
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x='holiday', y='Average Users', hue='User Type', data=avg_usage_by_holiday_melted, palette='Set2', ax=ax2)
ax2.set_title('Average Bike Usage on Workdays vs Holidays')
ax2.set_xlabel('Day Type')
ax2.set_ylabel('Average Number of Users')
ax2.grid(True)

grouped_df = day_df.groupby(by=["workingday", "season"]).agg({
    "cnt": ["mean"]
}).reset_index()

grouped_df.columns = ['workingday', 'season', 'mean_cnt']

plt.figure(figsize=(10, 6))
bar_width = 0.35
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
season_idx = np.arange(len(seasons))

grp_working = grouped_df[grouped_df['workingday'] == 1]
plt.bar(season_idx - bar_width/2, grp_working['mean_cnt'], bar_width, label='Workday', color='skyblue')
grp_holiday = grouped_df[grouped_df['workingday'] == 0]
plt.bar(season_idx + bar_width/2, grp_holiday['mean_cnt'], bar_width, label='Weekend', color='lightcoral')

plt.title('Average Bike usage by Season and Day Type')
plt.xlabel('Musim')
plt.ylabel('Average Bike usage')
plt.xticks(ticks=season_idx, labels=seasons)
plt.legend(title='Day Type')
plt.tight_layout()
fig3 = plt.gcf()

# Tambahan visualisasi 1: Jumlah penyewa sepeda berdasarkan musim
season_pattern = day_df.groupby(by="season")[["registered", "casual"]].sum().reset_index()
fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.bar(season_pattern["season"], season_pattern["registered"], label="Registered", color="blue")
ax4.bar(season_pattern["season"], season_pattern["casual"], bottom=season_pattern["registered"], label="Casual", color="red")
ax4.set_xlabel("Season")
ax4.set_ylabel("Number of Users")
ax4.set_title("Jumlah Penyewa Sepeda Berdasarkan Musim")
ax4.legend()

# Tambahan visualisasi 2: Perbandingan penyewa sepeda setiap hari
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="weekday",
    y="cnt",
    data=day_df,
    order=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    palette="viridis",
    ax=ax5
)
ax5.set_title('Perbandingan Penyewa Sepeda Setiap Hari')
ax5.set_xlabel(None)
ax5.set_ylabel('Jumlah Pengguna Sepeda')
ax5.grid(True)

# st.header("Hasil Analisis Penyewa Sepeda")
# st.write("\n")
# st.subheader("Grafik Rata-rata Tipe Penyewa berdasarkan tipe Penyewa")
# st.write("Grafik di bawah ini menunjukkan rata-rata tipe pengguna sewa sepeda berdasarkan bulan untuk untuk melihat perbandingan tipe pengguna casual(tidak terdaftar) dan registered(terdaftar)")
# st.pyplot(fig1, use_container_width=True)

# st.write("\n")
# st.subheader("Grafik Rata-rata Penyewa Berdasarkan Tipe Hari")
# st.write("Grafik di bawah ini menunjukkan rata-rata pengguna sewa sepeda berdasarkan tipe hari (Hari Kerja atau Akhir Pekan)")
# st.pyplot(fig2, use_container_width=True)
st.write("\n")
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Musim")
st.write("Grafik di bawah ini menunjukkan jumlah penyewa sepeda berdasarkan musim untuk tipe pengguna terdaftar dan tidak terdaftar.")
st.pyplot(fig4, use_container_width=True)

st.write("\n")
st.subheader("Grafik Rata-rata Penyewa Sepeda setiap hari Tipe Hari")
st.write("Grafik di bawah ini menunjukkan rata-rata pengguna sewa sepeda berdasarkan musim (Spring, Summer, Fall, Winter) dan tipe hari (Hari Kerja atau Akhir Pekan). Ini membantu memahami perbedaan jumlah penyewa sepeda pada hari kerja dibandingkan akhir pekan, serta variasi berdasarkan musim.")
st.pyplot(fig3, use_container_width=True)



st.write("\n")
st.subheader("Perbandingan Penyewa Sepeda Setiap Hari")
st.write("Grafik di bawah ini menunjukkan perbandingan jumlah penyewa sepeda setiap hari dalam seminggu.")
st.pyplot(fig5, use_container_width=True)
