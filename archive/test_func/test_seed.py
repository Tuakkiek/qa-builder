import random 

def test_seed(seed_value): 
    random.seed(seed_value)

    numbers = []
    for _ in range(7): 
        numbers.append(random.randint(1, 100))

    return numbers

for i in range(1, 20): 
    if i > 10: 
        print(test_seed(99))
    else: 
        print(test_seed(42))

    
