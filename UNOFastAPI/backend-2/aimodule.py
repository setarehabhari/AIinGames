import rlcard
from rlcard import models
from rlcard.agents.human_agents.uno_human_agent import HumanAgent, _print_action

# Make environment
env = rlcard.make('uno')
human_agent = HumanAgent(env.num_actions)
cfr_agent = models.load('uno-rule-v1').agents[0]
env.set_agents([
    human_agent,
    cfr_agent,
])

print(">> UNO rule model V1")