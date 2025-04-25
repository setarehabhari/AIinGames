@echo off

REM Run evaluations in parallel
start "" python evaluate.py --models random random
start "" python evaluate.py --models random DMC0_1_000_000.pth
start "" python evaluate.py --models random DMC1_10_000_000.pth
start "" python evaluate.py --models random DQN1Model.pth
start "" python evaluate.py --models random DQN2Model.pth

start "" python evaluate.py --models DQN1Model.pth DQN2Model.pth
start "" python evaluate.py --models DQN1Model.pth DMC0_1_000_000.pth
start "" python evaluate.py --models DQN1Model.pth DMC1_10_000_000.pth

start "" python evaluate.py --models DQN2Model.pth DMC0_1_000_000.pth
start "" python evaluate.py --models DQN2Model.pth DMC1_10_000_000.pth

start "" python evaluate.py --models DMC0_1_000_000.pth DMC1_10_000_000.pth

REM Optional: wait for user input to close the window
pause
