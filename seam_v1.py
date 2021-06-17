


import sys

from energy import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


def compute_vertical_seam_v1(energy_data):
    #this function finds the lowest energy seam given the energy at each pixel.

    m_grid = [[0 for _ in row] for row in energy_data]        # creating grid same in size as image n init to 0

    h = len(energy_data)
    w = len(energy_data[0])  #since image is list of lists 

    for x in range(w):
        m_grid[0][x] = energy_data[0][x]           # we fill the top row (BASE CASE) as is.

    for y in range(h):
        for x in range(w):
            x_min = x-1 if x > 0 else 0  # we are checking if x is at say left boundary, then we are not supposed to check for bottom-left, we only check bottom and bottom-right
            x_max = x+1 if x < w-1 else w-1 

            min_parent_energy = min(m_grid[y-1][x_candidate] for x_candidate in range(x_min, x_max+1))   # we check all three possibilities(bottom, bottom-left, bottom-right) and take min of 'em

            m_grid[y][x] = energy_data[y][x] + min_parent_energy

    min_end_x, min_seam_energy = min(enumerate(m_grid[h-1]), key=lambda m:m[1])       #iterating the last row and picking the x coordinate with lowest seam value.

    return (min_end_x, min_seam_energy)

    raise NotImplementedError('compute_vertical_seam_v1 is not implemented')


def visualize_seam_end_on_image(pixels, end_x):

    #this function draws red box over the lowest seam coordinate. 

    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    min_x = max(end_x - 5, 0)
    max_x = min(end_x + 5, w - 1)

    min_y = max(h - 11, 0)
    max_y = h - 1

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            new_pixels[y][x] = Color(255, 0, 0)

    return new_pixels


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)

    print('Finding the lowest-energy seam...')
    min_end_x, min_seam_energy = compute_vertical_seam_v1(energy_data)

    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_end_on_image(pixels, min_end_x)
    write_array_into_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {min_end_x}')
