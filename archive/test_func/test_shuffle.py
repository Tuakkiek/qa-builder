#import thư viện random để xáo trộn danh sách.
import random 

#def hàm xáo trộn danh sách mà không làm thay đổi danh sách gốc.
def test_shuffle(data: list, seed: int | None = None) -> list:

    #tạo một bản sao (copy) của danh sách để tránh thay đổi dữ liệu gốc.
    data_copy = data.copy()

    #nếu có truyền seed thì cố định seed ngẫu nhiên.
    if seed is not None:
        random.seed(seed)
    #xáo trộn danh sách bản sao tại chỗ.
    random.shuffle(data_copy)

    #trả về danh sách đã được xáo trộn.
    return data_copy

#danh sách dữ liệu số nguyên ban đầu từ 1 đến 10.
original_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#chạy thử 10 lần xáo trộn với 2 seed khác nhau (42 và 99).
for i in range(10):
    #từ lần thứ 6 trở đi dùng seed 99.
    if i > 5:
        print(test_shuffle(original_data, 99))     
    #5 lần đầu dùng seed 42 (kết quả các lần này sẽ luôn giống hệt nhau).
    else: 
        print(test_shuffle(original_data, 42))
    