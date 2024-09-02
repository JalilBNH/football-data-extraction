import cv2
from colorthief import ColorThief
import os 
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import numpy as np

path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\cropped_players'
points = []
for i, file in enumerate(os.listdir(path)):
    color_thief = ColorThief(os.path.join(path, file))
    dominant_color = color_thief.get_color(quality=1)
    palette_color = color_thief.get_palette(color_count=3)
    print(f'image: {i}, color : {[c for c in dominant_color]}, color_palette : {palette_color}')
    points.append(dominant_color)

idx = 1
x_vals = [point[0] for point in points]
y_vals = [point[1] for point in points]
z_vals = [point[2] for point in points]
print(x_vals)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x_vals, y_vals, z_vals, marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

for i, (x,y,z) in enumerate(points):
    ax.text(x, y, z, f'{i+1}', color='red')
    
kmeans = KMeans(n_clusters=2, n_init='auto', random_state=0).fit(points)
print(kmeans.labels_)


path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\cropped_players'
color_means = []


for file in os.listdir(path):
    image = plt.imread(os.path.join(path, file))
    sum_r = 0
    sum_g = 0
    sum_b = 0
    card = image.shape[0] * image.shape[1]
    for rows in image:
        for cols in rows:
            sum_r += cols[0]
            sum_g += cols[1]
            sum_b += cols[2]
    color_means.append((int(sum_r/card), int(sum_g/card), int(sum_b/card)))

for color in color_means:
    print(color)
    

x_vals = [color[0] for color in color_means]
y_vals = [color[1] for color in color_means]
z_vals = [color[2] for color in color_means]
print(x_vals)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x_vals, y_vals, z_vals, marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

for i, (x,y,z) in enumerate(color_means):
    ax.text(x, y, z, f'{i+1}', color='red')
    
plt.show()