import random
import copy
import math
import Utility
from operator import attrgetter
from PIL import Image
from Pixel import Pixel


class KMeans:

    def __init__(self, image: Image, matrix, k: int):
        self.image = image
        self.matrix = matrix
        self.width, self.height = image.size
        self.k = k
        self.prev_centroid_list = list()
        self.centroid_list = list()
        self.clustered_pixel_dict = dict()

    def cluster_image(self):
        keep_clustering = True
        count = 0
        self.centroid_list = self.generate_random_centroids()
        print(f'Initial Random Centroids:')
        Utility.print_iterable(self.centroid_list)
        while keep_clustering:
            self.clustered_pixel_dict = self.calculate_k_means()
            self.prev_centroid_list = copy.deepcopy(self.centroid_list)
            for centroid in self.centroid_list:
                centroid.color = self.calculate_optimal_centroid(centroid)
            if self.prev_centroid_list == self.centroid_list:
                keep_clustering = False
            # if count % 10 == 0:
            print(f'K-Means iteration {count}')
            count += 1
        print(f'Optimal centroids found after {count} iterations')
        self.prev_centroid_list = copy.deepcopy(self.centroid_list)

    def generate_random_centroids(self) -> list:
        centroid_set = set()
        while len(centroid_set) < self.k:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            color = self.matrix[x, y]
            centroid_set.add(Pixel(x, y, color))
        centroid_list = list(centroid_set)
        if len(self.prev_centroid_list) == 0:
            i = 1
            for centroid in centroid_list:
                centroid.cluster_assignment = i
                i += 1
        else:  # aligns the newly generated centroids clusters with the previous centroids clusters
            temp_clusters = list()
            for i in range(self.k):
                temp_clusters.append(0)
            for i in range(self.k):
                prev_dist = None
                for j in range(self.k):
                    if self.prev_centroid_list[j].cluster_assignment not in temp_clusters:
                        dist = math.dist(self.prev_centroid_list[j].color, centroid_list[i].color)
                        if prev_dist is None:
                            prev_dist = dist
                            temp_clusters[i] = self.prev_centroid_list[j].cluster_assignment
                        elif dist < prev_dist:
                            prev_dist = dist
                            temp_clusters[i] = self.prev_centroid_list[j].cluster_assignment
                    else:
                        continue
            for i in range(self.k):
                centroid_list[i].cluster_assignment = temp_clusters[i]
        return sorted(centroid_list, key=attrgetter('cluster_assignment'))

    def calculate_optimal_centroid(self, centroid: Pixel) -> tuple:
        red = list()
        green = list()
        blue = list()
        count = 0
        for pixel in self.clustered_pixel_dict[centroid.cluster_assignment]:
            red.append(pixel.color[0])
            green.append(pixel.color[1])
            blue.append(pixel.color[2])
            count += 1
        if count == 0:
            return centroid.color
        avg_red = sum(red) / count
        avg_green = sum(green) / count
        avg_blue = sum(blue) / count
        return avg_red, avg_green, avg_blue

    def calculate_k_means(self) -> dict:
        pixel_dict = dict()
        for i in range(self.k):
            pixel_dict[i + 1] = list()
        for y in range(self.height):
            for x in range(self.width):
                cluster_assignment = self.calculate_closest_cluster(self.matrix[x, y])
                pixel_dict[cluster_assignment].append(Pixel(x, y, self.matrix[x, y], cluster_assignment))
        return pixel_dict

    def calculate_closest_cluster(self, pixel_color: tuple) -> int:
        prev_distance = None
        cluster_assignment = 0
        for centroid in self.centroid_list:
            distance = math.dist(pixel_color, centroid.color)
            if prev_distance is None:
                prev_distance = distance
                cluster_assignment = centroid.cluster_assignment
            elif distance < prev_distance:
                prev_distance = distance
                cluster_assignment = centroid.cluster_assignment
        return cluster_assignment
