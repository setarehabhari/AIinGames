import subprocess
import sys
from distutils.version import LooseVersion

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

if 'torch' in installed_packages:
    from UNOFastAPI.rlcard.agents.dqn_agent import DQNAgent as DQNAgent
    from UNOFastAPI.rlcard.agents.nfsp_agent import NFSPAgent as NFSPAgent

from UNOFastAPI.rlcard.agents.cfr_agent import CFRAgent
from UNOFastAPI.rlcard.agents.human_agents.limit_holdem_human_agent import HumanAgent as LimitholdemHumanAgent
from UNOFastAPI.rlcard.agents.human_agents.nolimit_holdem_human_agent import HumanAgent as NolimitholdemHumanAgent
from UNOFastAPI.rlcard.agents.human_agents.leduc_holdem_human_agent import HumanAgent as LeducholdemHumanAgent
from UNOFastAPI.rlcard.agents.human_agents.blackjack_human_agent import HumanAgent as BlackjackHumanAgent
from UNOFastAPI.rlcard.agents.human_agents.uno_human_agent import HumanAgent as UnoHumanAgent
from UNOFastAPI.rlcard.agents.random_agent import RandomAgent
