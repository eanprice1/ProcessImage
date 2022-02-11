import Utility
from KMeans import KMeans
from PIL import Image


def main():
    # comment line 8 and uncomment line 9 to test small images
    image_names = ['natureImage.jfif', 'selfie.jpg']
    # image_names = ['testing.jfif']
    for image_name in image_names:
        k = 10
        num_of_execs = 1
        print(f'Image Name: {image_name}')
        print(f'K = {k}')
        image = Image.open(f'Resources/{image_name}')
        matrix = image.load()
        kmeans = KMeans(image, matrix, k)
        layered_pixel_list = list()
        centroid_lists = list()
        for i in range(num_of_execs):
            print(f'\nExecution Number: {i}')
            kmeans.cluster_image()
            layered_pixel_list.append(kmeans.clustered_pixel_dict)
            centroid_lists.append(kmeans.centroid_list)
            print(f'Optimal Centroids for Execution {i}: ')
            Utility.print_iterable(kmeans.centroid_list)

        # I was not 100% sure what the probability map was or what needed to be done to create it.
        # The below code was my best idea of what was wanted for the end product.
        # created new images based off of the clusters generated from the images
        for i in range(num_of_execs):
            for j in range(k):
                centroid = centroid_lists[i][j]
                rgb = centroid.color
                rgb = (int(round(rgb[0])), int(round(rgb[1])), int(round(rgb[2])))
                count = 0
                for pixel in layered_pixel_list[i][centroid.cluster_assignment]:
                    matrix[pixel.loc_x, pixel.loc_y] = rgb
                    count += 1
            image.save(f'Outputs/result{i}{image_name}')


if __name__ == "__main__":
    main()
