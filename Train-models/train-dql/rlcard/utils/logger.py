import os
import csv

class Logger(object):
    ''' Logger saves the running results and helps make plots from the results
    '''

    def __init__(self, log_dir, runName):
        ''' Initialize the labels, legend and paths of the plot and log file.

        Args:
            log_path (str): The path the log files
        '''
        self.log_dir = log_dir
        self.id = runName

    def __enter__(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.txt_path = os.path.join(self.log_dir, f'log_{self.id}.txt')
        self.csv_path = os.path.join(self.log_dir, f'performance_{self.id}.csv')
        self.fig_path = os.path.join(self.log_dir, f'fig_{self.id}.png')
        self.rl_path = os.path.join(self.log_dir, f'rl-loss_{self.id}.txt')
        self.rl_csv_path = os.path.join(self.log_dir, f'rl-loss-performance_{self.id}.csv')
        self.rl_fig = os.path.join(self.log_dir, f'rl-loss-fig_{self.id}.png')

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.txt_file = open(self.txt_path, 'w')
        self.csv_file = open(self.csv_path, 'w')
        self.rl_file = open(self.rl_path, 'w')
        self.rl_csv_file = open(self.rl_csv_path, 'w')
        fieldnames = ['episode', 'reward']
        rlFieldnames = ['step','rl-loss', 'episode']
        self.writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.rlwriter = csv.DictWriter(self.rl_csv_file, fieldnames=rlFieldnames)
        self.writer.writeheader()
        self.rlwriter.writeheader()

        return self

    def log(self, text):
        ''' Write the text to log file then print it.
        Args:
            text(string): text to log
        '''
        self.txt_file.write(text+'\n')
        self.txt_file.flush()
        #print(text)

    def logrl(self, text):
        ''' Write the text to log file then print it.
        Args:
            text(string): text to log
        '''
        self.rl_file.write(str(text))
        self.rl_file.write('\n')
        self.rl_file.flush()
        #print(text)

    def log_rlloss(self, step, rlloss, episode):
        self.rlwriter.writerow({'step':step, 'rl-loss':rlloss, 'episode':episode})
        self.rl_file.write(str(rlloss))
        self.rl_file.write('\n')
        self.rl_file.flush()

    def log_performance(self, episode, reward):
        ''' Log a point in the curve
        Args:
            episode (int): the episode of the current point
            reward (float): the reward of the current point
        '''
        self.writer.writerow({'episode': episode, 'reward': reward})
        print('')
        self.log('----------------------------------------')
        self.log('  episode      |  ' + str(episode))
        self.log('  reward       |  ' + str(reward))
        self.log('----------------------------------------')

    def __exit__(self, type, value, traceback):
        if self.txt_path is not None:
            self.txt_file.close()
        if self.csv_path is not None:
            self.csv_file.close()
        if self.rl_csv_path is not None:
            self.rl_csv_file.close()
        if self.rl_path is not None:
            self.rl_file.close()
        print('\nLogs saved in', self.log_dir)
