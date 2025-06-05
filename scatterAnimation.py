import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import psutil

x_min = float("inf")
x_max = 0
y_min = float("inf")
y_max = 0
val_min = float('inf')
val_max = 0

idx = 0

filename = ""
while not os.path.exists(filename):
    filename = input("Enter .dat/.DAT filename: ")
    name, ext = filename.split('.')

    if ext.lower() != "dat":
        print("Please enter a .dat/.DAT file.")
        filename = ""

    elif not os.path.exists(filename):
        print("The file entered is not in the current directory, please reenter.")

print("opening file...", end="", flush=True)

with open(filename, "r") as file:
    tot_lines = 0
    for line in file:
        tot_lines += 1
        parts = line.strip().split()
        x = float(parts[0])
        y = float(parts[1])
        val = float(parts[4])

        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x

        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y

        if val > val_max:
            val_max = val
        if val < val_min:
            val_min = val

    print("50%...", end="", flush=True)

    width = 328
    length = 601
    depth = tot_lines / 197128
    if depth != round(depth):
        raise ValueError("file does not contain an even amount of visual slices")
    depth = int(depth)

    # reset file pointer to iterate again
    file.seek(0)

    frames = []
    for k in range(depth):
        x, y, val = [], [], []
        for i in range(width * length):
            line = file.readline()
            parts = line.strip().split()
            x.append(float(parts[0]))
            y.append(float(parts[1]))
            val.append(float(parts[4]))
        frames.append((np.array(x), np.array(y), np.array(val)))

    print("100%")

# check memory usage
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")

# Create the plot
fig, ax = plt.subplots()
sc = ax.scatter([], [], c=[], cmap="coolwarm", s=0.1, vmin=val_min, vmax=val_max)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
plt.colorbar(sc, label="Temperature")


def update(frame_index):
    x, y, val = frames[frame_index]
    sc.set_offsets(np.column_stack((x, y)))
    sc.set_array(val)
    return (sc,)


ani = animation.FuncAnimation(fig, update, frames=depth, interval=100, blit=True)
plt.show()
