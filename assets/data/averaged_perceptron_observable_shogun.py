from shogun import csv_file, features, labels, machine, parameter_observer

f_feats_train = csv_file("classifier_binary_2d_linear_features_train.dat")
f_feats_test = csv_file("classifier_binary_2d_linear_features_test.dat")
f_labels_train = csv_file("classifier_binary_2d_linear_labels_train.dat")
f_labels_test = csv_file("classifier_binary_2d_linear_labels_test.dat")

features_train = features(f_feats_train)
features_test = features(f_feats_test)
labels_train = labels(f_labels_train)
labels_test = labels(f_labels_test)

perceptron = machine("AveragedPerceptron", labels=labels_train, learn_rate=1.0, max_iterations=10)

observer = parameter_observer("ParameterObserverLogger")
perceptron.subscribe(observer)

perceptron.train(features_train)
labels_predict = perceptron.apply(features_test)

perceptron.get("bias")

#
# Code for producing the animation
#
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])

plt.suptitle("Binary Data Sample")

# We first need to divide the samples into one class
# and the other
blue_x = []
red_x = []
blue_y = []
red_y = []

for i in range(0, features_train.get_num_vectors()):
    mat = features_train.get("feature_matrix")
    if (labels_train.get("labels")[i] == 1):
        blue_x.append(mat[0][i])
        blue_y.append(mat[1][i])
    else:
        red_x.append(mat[0][i])
        red_y.append(mat[1][i])

# Divide the observations into bias and weigths
w = []
bias = []
for i in range(0, observer.get("num_observations")):
    if (observer.get_observation(i).get("name") == "w"):
        w.append(observer.get_observation(i).get("w"))
    elif (observer.get_observation(i).get("name") == "bias"):
        bias.append(observer.get_observation(i).get("bias"))

# Plot the background for each frame
def init():

    plt.plot(blue_x, blue_y, 'bo', label="Label = 1")
    plt.plot(red_x, red_y, 'ro', label="Label = -1")

    line.set_data([], [])
    line.set_label("hyperplane")

    plt.xlabel("x")
    plt.ylabel("y")

    return line,

# Print the observation line on screen
def animate(i):
    print("Processing observation: {}/{}".format(i, len(w)))
    plt.title("Iteration {}".format(i))
    x = np.linspace(-10, 10, 1000)
    line.set_data(x, x*w[i][0]+x*w[i][1]+bias[i])

    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(w), interval=200, blit=True)
anim.save('./video/hyperplane.mp4', fps=30, extra_args=['-vcodec', 'libx264'], bitrate=500)
