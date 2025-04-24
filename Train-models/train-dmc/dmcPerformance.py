import os
import pandas as pd
import matplotlib.pyplot as plt

def summarize_dmc_logs(log_dir):
    summaries = []
    for run in os.listdir(log_dir):
        run_path = os.path.join(log_dir, run, 'logs.csv')
        if not os.path.isfile(run_path):
            continue
        df = pd.read_csv(run_path)
        if df.empty:
            continue

        # Get the last row of the DataFrame
        last_row = df.iloc[-1]
        
        # Calculate the mean reward for both agents
        #print(df['mean_episode_return_0'])
        mean_reward_0 = df['mean_episode_return_0'].mean()
        mean_reward_1 = df['mean_episode_return_1'].mean()

        summaries.append({
            'Run': run,
            'Frame': last_row['frames'],
            'Reward_0': round(last_row['mean_episode_return_0'], 4),
            'Reward_1': round(last_row['mean_episode_return_0'], 4),
            'avgReward_0': round(mean_reward_0, 4),
            'avgReward_1': round(mean_reward_1, 4)
        })

        # Plotting the rewards over time for both agents
        plt.plot(df['frames'], df['mean_episode_return_0'], label='Agent 0', color='b')
        plt.plot(df['frames'], df['mean_episode_return_1'], label='Agent 1', color='g')

        # Save the plot with the run name
        chart_filename = os.path.join(log_dir, run, f'{run}_reward_plot.png')
        plt.xlabel('Frames')
        plt.ylabel('Mean Episode Return')
        plt.title(f'Mean Episode Return for {run}')
        plt.legend(loc='best')
        plt.savefig(chart_filename)  # Save the chart as a PNG file
        plt.clf()  # Clear the plot for the next run

    summaries.sort(key=lambda x: x['Reward_0'], reverse=True)
    
    # Print out the summarized results
    print(f"{'Run':<40} {'Frame':>10} {'Reward_0':>10} {'Reward_1':>10} {'avgReward_0':>10} {'avgReward_1':>10}")
    print("-" * 80)
    for s in summaries:
        print(f"{s['Run']:<40} {s['Frame']:>10} {s['Reward_0']:>10} {s['Reward_1']:>10} {s['avgReward_0']:>10} {s['avgReward_1']:>10}")

# Example usage
if __name__ == '__main__':
    # print("GPU\n")
    # summarize_dmc_logs('experiments/uno_dmc_grid_4_22_3') 
    # print("CPU\n") 
    # summarize_dmc_logs('experiments/uno_dmc_grid_4_22_4CPU')  
    # print("CPU2\n")
    summarize_dmc_logs('experiments/uno_dmc_grid_22_22_46_')  


