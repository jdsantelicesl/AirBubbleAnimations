import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
from scipy.interpolate import griddata


x_min = float("inf")
x_max = 0
y_min = float("inf")
y_max = 0
val_min = float("inf")
val_max = 0

print("loading file...")

with open("zz_test1.dat", "r") as file:
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

            # ignore noise data
            if float(parts[4]) < 299.5 or float(parts[4]) > 300.5:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
                val.append(float(parts[4]))

        frames.append((np.array(x), np.array(y), np.array(val)))

    print("100%")

# Smaller window values
# x_min = -1000
# x_max = 4000
# y_max = 5000
# y_min = 0

# contour definition detail level. Higher is better defined
definition = 1000

# Create a grid to interpolate onto
grid_x, grid_y = np.meshgrid(
    np.linspace(x_min, x_max, definition), np.linspace(y_min, y_max, definition)
)


print("\nInterpolating contour plot values...")

# Interpolate z-values onto grid
grid_z_arr = []

# load all z grids into an array so save compute time at rendering
for i in range(depth):
    grid_z_arr.append(
        griddata(
            (frames[i][0], frames[i][1]), frames[i][2], (grid_x, grid_y), method="cubic"
        )
    )
    
    # Display percentage completion
    if i % (depth // 10) == 0:
        print(f"{int((i/depth)*100)}%...", end="\r", flush=True)

print("finished interpolating")


fig, ax = plt.subplots()
cp = ax.contour(grid_x, grid_y, grid_z_arr[0], levels=20, cmap="coolwarm")
# cbar = fig.colorbar(cp)
ax.set_title("Contour Plot from (x, y, value)")
ax.set_xlabel("X")
ax.set_ylabel("Y")


def update(frame_index):

    # Remove old contour collections
    for coll in ax.collections:
        coll.remove()
    
    # redraw
    ax.contour(grid_x, grid_y, grid_z_arr[frame_index], levels=20, cmap="coolwarm")


# Animate
anim = FuncAnimation(fig, update, frames=len(frames), interval=300)

plt.show()
