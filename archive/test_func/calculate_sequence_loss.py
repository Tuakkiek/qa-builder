import math

def calculate_sequence_loss(probabilities): 

    losses = [] 
    for p in probabilities: 
        losses.append(-math.log(p))

    return losses

probs = [0.8, 0.7, 0.9, 0.8, 0.6, 0.9, 0.8]

individual_losses = calculate_sequence_loss(probs)

print("Loss của từng token:", individual_losses)
