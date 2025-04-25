import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os

def plotStats(directory):
    base_dir = './experiments'
    log_name = 'logs.csv'
    csv_file_path = os.path.join(base_dir, directory, log_name)
    print(f"Reading: {csv_file_path}")

    pngName = '_mean_episode_combined.png'
    output_name = str(directory) + pngName
    
    df = pd.read_csv(csv_file_path)

    mean_reward_0 = df['mean_episode_return_0'].mean()
    mean_reward_1 = df['mean_episode_return_1'].mean()
    print(f"mean_reward_0:{mean_reward_0}")
    print(f"mean_reward_1:{mean_reward_1}")

    max_reward_0 = df['mean_episode_return_0'].max()
    max_reward_1 = df['mean_episode_return_1'].max()
    print(f"max_reward_0:{max_reward_0}")
    print(f"max_reward_1:{max_reward_1}")

    min_reward_0 = df['mean_episode_return_0'].min()
    min_reward_1 = df['mean_episode_return_1'].min()
    print(f"min_reward_0:{min_reward_0}")
    print(f"min_reward_1:{min_reward_1}")

    # min and max of both so the plot is big enough
    min_return = min(df['mean_episode_return_0'].min(), df['mean_episode_return_1'].min())
    max_return = max(df['mean_episode_return_0'].max(), df['mean_episode_return_1'].max())

    # Combined plot
    plt.figure(figsize=(8, 6))
    plt.plot(df['frames'], df['mean_episode_return_0'], label="Return 0", color='blue')
    plt.plot(df['frames'], df['mean_episode_return_1'], label="Return 1", color='green')
    plt.xlabel('Frames')
    plt.ylabel('Mean Episode Return')
    plt.title('Mean Episode Return vs Frames')
    plt.grid(True)
    plt.ylim(min_return, max_return)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_name)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory within experiments")
    args = parser.parse_args()
    plotStats(args.directory)