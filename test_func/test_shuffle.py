import random 

def test_shuffle(data, seed=None):

    data_copy = data.copy()

    if seed is not None:
        random.seed(seed)
    random.shuffle(data_copy)

    return data_copy

original_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in range(10):
    if i > 5:
        print(test_shuffle(original_data, 99))     
    else: 
        print(test_shuffle(original_data, 42))
    