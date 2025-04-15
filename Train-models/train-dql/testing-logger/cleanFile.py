import re
import matplotlib.pyplot as plt

steps = []
losses = []

pattern = re.compile(r"INFO - Step (\d+), rl-loss: ([\d\.eE+-]+)")

with open('4-15-00h05m.log', 'r', encoding='utf-16') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        match = pattern.search(line)
        if match:
            steps.append(int(match.group(1)))
            losses.append(float(match.group(2)))

# Plot and save
plt.plot(steps, losses)
plt.xlabel("Step")
plt.ylabel("RL Loss")
plt.title("RL Loss Over Steps")
plt.grid(True)
plt.savefig("rl_loss_plot.png")

# Min and max with steps
min_loss = min(losses)
max_loss = max(losses)
min_step = steps[losses.index(min_loss)]
max_step = steps[losses.index(max_loss)]

with open("output.txt", "w") as out:
    out.write(f"Min RL Loss: {min_loss:.6f} at Step {min_step}\n")
    out.write(f"Max RL Loss: {max_loss:.6f} at Step {max_step}\n")
