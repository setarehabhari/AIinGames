import torch
from rlcard.agents.dqn_agent import DQNAgent  # Ensure the class is imported

torch.serialization.add_safe_globals([DQNAgent])  # Allow the blocked class
data = torch.load("model.pth", weights_only=False)
print(data)

# policy_data = data.get("policy", {})
# average_policy_data = data.get("average_policy", {})
# regrets_data = data.get("regrets", {})
# iteration = data.get("iteration", 0)

# # Convert tensors to numpy arrays (if necessary)
# import numpy as np
# for key in policy_data:
#     policy_data[key] = policy_data[key].numpy() if isinstance(policy_data[key], torch.Tensor) else policy_data[key]

# for key in average_policy_data:
#     average_policy_data[key] = average_policy_data[key].numpy() if isinstance(average_policy_data[key], torch.Tensor) else average_policy_data[key]

# for key in regrets_data:
#     regrets_data[key] = regrets_data[key].numpy() if isinstance(regrets_data[key], torch.Tensor) else regrets_data[key]

# # Save as pickle to match CFR format
# import pickle

# with open("policy.pkl", "wb") as f:
#     pickle.dump(policy_data, f)

# with open("average_policy.pkl", "wb") as f:
#     pickle.dump(average_policy_data, f)

# with open("regrets.pkl", "wb") as f:
#     pickle.dump(regrets_data, f)

# with open("iteration.pkl", "wb") as f:
#     pickle.dump(iteration, f)

# print("Converted and saved in CFR format")