#đoạn code tính toán hàm mất mát (loss)
import math

#def hàm tính toán giá trị mất mát (loss) cho một chuỗi các xác suất.
def calculate_sequence_loss(probabilities): 

    #tạo list rỗng để chứa kết quả loss của từng phần tử.
    losses = [] 

    #duyệt qua từng giá trị xác suất (p) trong danh sách đầu vào.
    for p in probabilities: 
        #tính âm logarit tự nhiên (-ln) của xác suất và thêm vào list kết quả.
        losses.append(-math.log(p))

    #trả về danh sách chứa các giá trị loss đã tính.
    return losses


#Code test tạo dữ liệu giả.
#tạo list mẫu chứa các xác suất dự đoán của từng token (ví dụ: mô hình tự tin 80%, 70%...).
probs = [0.8, 0.7, 0.9, 0.8, 0.6, 0.9, 0.8]


#gọi hàm để tính toán loss cho list xác suất mẫu.
individual_losses = calculate_sequence_loss(probs)


#in danh sách các giá trị loss tương ứng ra màn hình.
print("Loss của từng token:", individual_losses)