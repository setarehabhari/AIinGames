import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def parse_params(run_name):
    params = {}
    parts = run_name.split('_')
    for part in parts:
        if part.startswith('lr'):
            params['lr'] = float(part.replace('lr', ''))
        elif part.startswith('eps'):
            params['eps'] = float(part.replace('eps', ''))
        elif part.startswith('bs'):
            params['batch_size'] = int(part.replace('bs', ''))
        elif part.startswith('ul'):
            params['ul'] = int(part.replace('ul', ''))
    return params

def summarize_dmc_logs_grouped(log_dir):
    param_data = defaultdict(lambda: defaultdict(list))
    summary_lines = []

    for run in os.listdir(log_dir):
        run_path = os.path.join(log_dir, run, 'logs.csv')
        if not os.path.isfile(run_path):
            continue

        df = pd.read_csv(run_path)
        if df.empty:
            continue

        params = parse_params(run)
        mean_reward_0 = df['mean_episode_return_0'].mean()

        for param, value in params.items():
            param_data[param][value].append(mean_reward_0)

        plt.plot(df['frames'], df['mean_episode_return_0'], label='Agent 0', color='b')
        plt.plot(df['frames'], df['mean_episode_return_1'], label='Agent 1', color='g')
        plt.xlabel('Frames')
        plt.ylabel('Mean Episode Return')
        plt.title(f'Mean Return for {run}')
        plt.legend()
        plt.savefig(os.path.join(log_dir, run, f'{run}_reward_plot.png'))
        plt.clf()

    for param, values in param_data.items():
        summary_lines.append(f"=== {param} ===")
        for val, rewards in sorted(values.items()):
            avg_r = np.mean(rewards)
            max_r = np.max(rewards)
            summary_lines.append(f"{param}={val} | Avg Reward: {avg_r:.4f} | Max Reward: {max_r:.4f}")
        summary_lines.append("\n" + "="*50 + "\n")

    with open("dmc_param_summary.txt", "w") as f:
        f.write("\n".join(summary_lines))

# Run the summarizer
if __name__ == '__main__':
    summarize_dmc_logs_grouped('experiments/uno_dmc_grid_22_22_46_')
