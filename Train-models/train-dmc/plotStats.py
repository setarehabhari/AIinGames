import matplotlib.pyplot as plt
import pandas as pd

# Replace this with the path to your CSV file
csv_file_path = 'logs.csv'

# Load the data from the CSV file
df = pd.read_csv(csv_file_path)

# Get the min and max values for mean_episode_return and loss for y-axis scaling
min_return = min(df['mean_episode_return_0'].min(), df['mean_episode_return_1'].min())
max_return = max(df['mean_episode_return_0'].max(), df['mean_episode_return_1'].max())

min_loss = min(df['loss_0'].min(), df['loss_1'].min())
max_loss = max(df['loss_0'].max(), df['loss_1'].max())

# Plot Mean Episode Return
plt.figure(figsize=(12, 6))

# Plot mean_episode_return_0 (initial return)
plt.subplot(1, 2, 1)
plt.plot(df['frames'], df['mean_episode_return_0'], label="Mean Episode Return 0", color='blue')
plt.xlabel('Frames')
plt.ylabel('Mean Episode Return')
plt.title('Mean Episode Return vs Frames (0)')
plt.grid(True)
plt.ylim(min_return, max_return)  # Set fixed y-axis limits for mean_episode_return

# Plot mean_episode_return_1 (after training)
plt.subplot(1, 2, 2)
plt.plot(df['frames'], df['mean_episode_return_1'], label="Mean Episode Return 1", color='green')
plt.xlabel('Frames')
plt.ylabel('Mean Episode Return')
plt.title('Mean Episode Return vs Frames (1)')
plt.grid(True)
plt.ylim(min_return, max_return)  # Set fixed y-axis limits for mean_episode_return

# Display the plots for mean_episode_return
plt.tight_layout()
plt.show()

# Plot Loss
plt.figure(figsize=(12, 6))

# Plot loss_0
plt.subplot(1, 2, 1)
plt.plot(df['frames'], df['loss_0'], label="Loss 0", color='red')
plt.xlabel('Frames')
plt.ylabel('Loss')
plt.title('Loss vs Frames (0)')
plt.grid(True)
plt.ylim(min_loss, max_loss)  # Set fixed y-axis limits for loss

# Plot loss_1
plt.subplot(1, 2, 2)
plt.plot(df['frames'], df['loss_1'], label="Loss 1", color='orange')
plt.xlabel('Frames')
plt.ylabel('Loss')
plt.title('Loss vs Frames (1)')
plt.grid(True)
plt.ylim(min_loss, max_loss)  # Set fixed y-axis limits for loss

# Display the plots for loss
plt.tight_layout()
plt.show()
