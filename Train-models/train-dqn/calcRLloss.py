import re
import matplotlib.pyplot as plt
import numpy as np

# this script is read the rl loss logs and then plot a smoothed version
def extract_rl_loss(filename):
    losses = []
    with open(filename, 'r', encoding='utf16') as file:
        for line in file:
            if "rl-loss:" in line:
                try:
                    value = float(line.split("rl-loss:")[1].strip())
                    losses.append(value)
                except (IndexError, ValueError):
                    continue
    return losses

def smooth_and_downsample(losses, window=1000, step=100):
    # Moving average
    smoothed = np.convolve(losses, np.ones(window)/window, mode='valid')
    # Downsampling
    return smoothed[::step]


def plot_losses(losses, figname, title="RL Loss"):
    plt.figure()
    plt.plot(losses)
    plt.title("RL Loss (Smoothed & Downsampled)")
    plt.xlabel("Step")
    plt.ylabel("RL Loss")
    plt.grid(True)
    plt.savefig(figname)

# no smoothing
def plot_raw_downsampled(losses, interval, figname, title="RL Loss (Raw Downsampled)"):
    downsampled = losses[::interval]
    plt.figure()
    plt.plot(downsampled, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(f"Every {interval} Steps")
    plt.ylabel("RL Loss")
    plt.grid(True)
    plt.savefig(figname)

def plot_losses_log(losses, figname, title="RL Loss (Log Scale)"):
    plt.figure()
    plt.plot(losses)
    plt.yscale('log')
    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("RL Loss (log scale)")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig(figname)


log_file_1 = './experiments/DQN1/DQN1rlLoss.log'
log_file_2 = './experiments/DQN2/DQN2rlLoss.log'
loss_values_1 = extract_rl_loss(log_file_1)
loss_values_2 = extract_rl_loss(log_file_2)

smoothed_1 = smooth_and_downsample(loss_values_1)
smoothed_2 = smooth_and_downsample(loss_values_2)
plot_losses(smoothed_1, "fig_DQN1_rl.png")
plot_losses(smoothed_2, "fig_DQN2_rl.png")

# Plot for first 10,000 steps
plot_losses(smoothed_1[:10000], "fig_DQN1_rl_10000.png", "DQN1 RL Loss (First 10000 Steps)")
plot_losses(smoothed_2[:10000], "fig_DQN2_rl_10000.png", "DQN2 RL Loss (First 10000 Steps)")

# Plot for steps 40,000 - 80,000
plot_losses(smoothed_1[400000:800000], "fig_DQN1_rl_400000_800000.png", "DQN1 RL Loss (Steps 400000-800000)")
plot_losses(smoothed_2[400000:800000], "fig_DQN2_rl_400000_800000.png", "DQN2 RL Loss (Steps 4000000-800000)")

# Plot raw losses every 10,000 steps (no smoothing)
plot_raw_downsampled(loss_values_1, 10000, "fig_DQN1_rl_raw.png", "DQN1 RL Loss (Raw Every 10,000 Steps)")
plot_raw_downsampled(loss_values_2, 10000, "fig_DQN2_rl_raw.png", "DQN2 RL Loss (Raw Every 10,000 Steps)")

# Log-scaled version of the full smoothed loss plot
plot_losses_log(smoothed_1, "fig_DQN1_rl_log.png", "DQN1 RL Loss (Smoothed, Log Scale)")
plot_losses_log(smoothed_2, "fig_DQN2_rl_log.png", "DQN2 RL Loss (Smoothed, Log Scale)")

avg_loss_1 = sum(loss_values_1) / len(loss_values_1)
avg_loss_2 = sum(loss_values_2) / len(loss_values_2)
print(f"DQN1 average loss: {avg_loss_1}")
print(f"DQN2 average loss: {avg_loss_2}")
