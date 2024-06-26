import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import imutils
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES

def get_color_name(rgb_tuple):
    min_colors = {}
    for key, name in CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = hex_to_rgb(key)
        rd = (r_c - rgb_tuple[0]) ** 2
        gd = (g_c - rgb_tuple[1]) ** 2
        bd = (b_c - rgb_tuple[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

clusters = 5 # try changing it

input_path = 'C:\\Local disk D\\most_dominant_color\\input_images\\IMG_3.jpg'
img = cv2.imread(input_path)
org_img = img.copy()
print('Org image shape --> ', img.shape)

img = imutils.resize(img, height=200)
print('After resizing shape --> ', img.shape)

flat_img = np.reshape(img, (-1, 3))
print('After Flattening shape --> ', flat_img.shape)

kmeans = KMeans(n_clusters=clusters, random_state=0)
kmeans.fit(flat_img)

dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint')

percentages = (np.unique(kmeans.labels_, return_counts=True)[1]) / flat_img.shape[0]
p_and_c = zip(percentages, dominant_colors)
p_and_c = sorted(p_and_c, reverse=True)

# Display color blocks with percentages and names
block = np.ones((50, 50, 3), dtype='uint')
plt.figure(figsize=(12, 8))
for i in range(clusters):
    plt.subplot(1, clusters, i + 1)
    block[:] = p_and_c[i][1][::-1]  # convert BGR to RGB
    plt.imshow(block)
    plt.xticks([])
    plt.yticks([])
    color_name = get_color_name(p_and_c[i][1][::-1])
    plt.xlabel(f"{color_name}\n{round(p_and_c[i][0] * 100, 2)}%")

# Display bar chart
bar = np.ones((50, 500, 3), dtype='uint')
plt.figure(figsize=(12, 8))
plt.title('Proportions of colors in the image')
start = 0
i = 1
for p, c in p_and_c:
    end = start + int(p * bar.shape[1])
    if i == clusters:
        bar[:, start:] = c[::-1]
    else:
        bar[:, start:end] = c[::-1]
    start = end
    i += 1

plt.imshow(bar)
plt.xticks([])
plt.yticks([])

rows = 1000
cols = int((org_img.shape[0] / org_img.shape[1]) * rows)
img = cv2.resize(org_img, dsize=(rows, cols), interpolation=cv2.INTER_LINEAR)

copy = img.copy()
cv2.rectangle(copy, (rows // 2 - 250, cols // 2 - 90), (rows // 2 + 250, cols // 2 + 110), (255, 255, 255), -1)

final = cv2.addWeighted(img, 0.1, copy, 0.9, 0)
cv2.putText(final, 'Most Dominant Colors in the Image', (rows // 2 - 230, cols // 2 - 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

start = rows // 2 - 220
for i in range(5):
    end = start + 70
    final[cols // 2:cols // 2 + 70, start:end] = p_and_c[i][1]
    cv2.putText(final, str(i + 1), (start + 25, cols // 2 + 45), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    start = end + 20

plt.show()

cv2.imshow('img', final)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Add "output" prefix to the original image name
output_dir = 'C:\\Local disk D\\most_dominant_color\\output_images\\'
base_name = os.path.basename(input_path)
output_name = f"output_{base_name}"
output_path = os.path.join(output_dir, output_name)

cv2.imwrite(output_path, final)
