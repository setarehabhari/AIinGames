''' Register new environments
'''
from UNOFastAPI.rlcard.envs.env import Env
from UNOFastAPI.rlcard.envs.registration import register, make

register(
    env_id='blackjack',
    entry_point='UNOFastAPI.rlcard.envs.blackjack:BlackjackEnv',
)

register(
    env_id='doudizhu',
    entry_point='UNOFastAPI.rlcard.envs.doudizhu:DoudizhuEnv',
)

register(
    env_id='limit-holdem',
    entry_point='UNOFastAPI.rlcard.envs.limitholdem:LimitholdemEnv',
)

register(
    env_id='no-limit-holdem',
    entry_point='UNOFastAPI.rlcard.envs.nolimitholdem:NolimitholdemEnv',
)

register(
    env_id='leduc-holdem',
    entry_point='UNOFastAPI.rlcard.envs.leducholdem:LeducholdemEnv'
)

register(
    env_id='uno',
    entry_point='UNOFastAPI.rlcard.envs.uno:UnoEnv',
)

register(
    env_id='mahjong',
    entry_point='UNOFastAPI.rlcard.envs.mahjong:MahjongEnv',
)

register(
    env_id='gin-rummy',
    entry_point='UNOFastAPI.rlcard.envs.gin_rummy:GinRummyEnv',
)

register(
    env_id='bridge',
    entry_point='UNOFastAPI.rlcard.envs.bridge:BridgeEnv',
)
