with open("sample.txt", "r", encoding="utf-8") as file: 
    text = file.read()

# Đếm số dòng 
line_count = len(text.splitlines())
# Đếm số từ 
word_count = len(text.split())
# In kết quả
print(f"Số dòng: {line_count}")
print(f"Số từ: {word_count}")