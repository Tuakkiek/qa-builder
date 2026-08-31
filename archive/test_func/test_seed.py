#import thư viện random sinh số ngẫu nhiên.
import random 

#def hàm sinh dãy 7 số ngẫu nhiên từ 1 đến 100 với seed chỉ định.
def test_seed(seed_value: int) -> list[int]: 
    #cố định hạt giống ngẫu nhiên (seed) để các lần sinh sau cho ra dãy số y hệt nhau.
    random.seed(seed_value)

    #tạo list chứa 7 số ngẫu nhiên.
    numbers = []
    for _ in range(7): 
        numbers.append(random.randint(1, 100))

    #trả về danh sách các số sinh ra.
    return numbers

#vòng lặp 19 lần để kiểm tra tính nhất quán của random seed.
for i in range(1, 20): 
    #từ lần thứ 11 trở đi dùng seed 99.
    if i > 10: 
        print(test_seed(99))
    #10 lần đầu dùng seed 42 (kết quả mỗi lần lặp sẽ luôn giống nhau).
    else: 
        print(test_seed(42))

    
