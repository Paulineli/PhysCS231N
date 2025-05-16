import numpy as np
import matplotlib.pyplot as plt

def plot_trajectory(trajectory, title='Trajectory'):
    plt.figure()
    plt.plot(trajectory[:, 0], trajectory[:, 1], label='Trajectory')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()