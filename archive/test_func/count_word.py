#def hàm dùng để đếm tổng số từ trong một đoạn văn bản.
def count_words(text: str) -> int: 
    #tách chuỗi theo khoảng trắng rồi đếm số lượng phần tử trả về.
    return len(text.split())

#đoạn văn bản mẫu để kiểm tra.
# text = "Python is esay, it is very popular and useful"

#in ra số lượng từ của đoạn văn bản mẫu.
# print(count_words(text))