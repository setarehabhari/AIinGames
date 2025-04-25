import csv

# this script is to calculate the final DQN agent max and average rewards
def calculate_rewards(filename):
    rewards = []
    
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header if there's one
        

        for row in csv_reader:
            if row != []:
                rewards.append(float(row[1]))  # Assuming reward is in the second column

    max_reward = max(rewards)
    avg_reward = sum(rewards) / len(rewards) if rewards else 0
    
    return max_reward, avg_reward

# Example usage
dqn1 = './experiments/DQN1/performance_DQNModel1.csv' 
dqn1_max_reward, dqn1_avg_reward = calculate_rewards(dqn1)
print(f"DQN1 Max Reward: {dqn1_max_reward}, DQN1 Average Reward: {dqn1_avg_reward}")

dqn2 = './experiments/DQN2/DQNModel2/performance_DQNModel2.csv' 
dqn2_max_reward, dqn2_avg_reward = calculate_rewards(dqn2)
print(f"DQN2 Max Reward: {dqn2_max_reward}, DQN2 Average Reward: {dqn2_avg_reward}")
