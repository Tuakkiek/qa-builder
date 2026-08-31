#mở file sample.txt và đọc file. 
#"with " là để đóng file tự động sau khi đọc xong.
with open("sample.txt", "r", encoding="utf-8") as file: 
    text = file.read()

# len() là hàm dùng để đếm.
# splitlines() là hàm dùng để tách các dòng.
# Đếm số dòng 
line_count = len(text.splitlines())

# split() là hàm dùng để tách các từ.
# Đếm số từ 
word_count = len(text.split())

# In kết quả
print(f"Số dòng: {line_count}")
print(f"Số từ: {word_count}")