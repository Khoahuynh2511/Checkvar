import streamlit as st
import pandas as pd

# Đọc dữ liệu từ file CSV
csv_file_path = 'chuyen_khoan.csv'

# Sử dụng st.cache_data để cache dữ liệu CSV
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = ['Ngày', 'Thứ Tự', 'Chuyển Khoản', 'Nội Dung']  # Đổi tên các cột cho phù hợp
    return df

# Load data
df = load_data(csv_file_path)

# Tiêu đề ứng dụng
st.title("Bảng sao kê giao dịch chuyển khoản")

# Tìm kiếm theo nội dung
search_query = st.text_input("Tìm kiếm theo nội dung", "")

# Lọc dữ liệu theo nội dung tìm kiếm
if search_query:
    df = df[df['Nội Dung'].str.contains(search_query, case=False, na=False)]

# Sắp xếp dữ liệu
sort_by = st.selectbox("Sắp xếp theo", ["Ngày", "Chuyển Khoản"])
sort_ascending = st.radio("Sắp xếp theo thứ tự", ["Tăng dần", "Giảm dần"])

if sort_ascending == "Tăng dần":
    df = df.sort_values(by=[sort_by], ascending=True)
else:
    df = df.sort_values(by=[sort_by], ascending=False)

# Hiển thị bảng dữ liệu
st.write(df)

# Thêm nút tải xuống file CSV đã lọc/sắp xếp
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df)

st.download_button(
    label="Tải xuống file CSV",
    data=csv,
    file_name='filtered_transactions.csv',
    mime='text/csv',
)
