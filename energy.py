import sys
from utils import Color, read_image_into_array, write_array_into_image

def energy_at(pixels, x, y):
    # computes the energy of the photo at given x,y position.

    h=len(pixels)
    w=len(pixels[0])  #since the image is rep as list of lists, we can get the height n width as follows.


    #now we figure out the left and right coordinates of the pixel
    x0 = x if x == 0 else x-1     #if x is at boundary at left
    x1 = x if x == w-1 else x+1     #boundary at right

    dxr = pixels[y][x0].r - pixels[y][x1].r
    dxg = pixels[y][x0].g - pixels[y][x1].g
    dxb = pixels[y][x0].b - pixels[y][x1].b
    dx = dxr*dxr + dxg*dxg + dxb*dxb


    y0 = y if y == 0 else y-1
    y1 = y if y == h-1 else y+1

    dyr = pixels[y0][x].r - pixels[y1][x].r
    dyg = pixels[y0][x].g - pixels[y1][x].g
    dyb = pixels[y0][x].b - pixels[y1][x].b
    dy = dyr*dyr + dyg*dyg + dyb*dyb


    return dx + dy



def compute_energy(pixels):
    #compute energy of image at each n every pixel

    energy = [[0 for _ in row] for row in pixels]   #we create a new 2D grid same in size as image, but all values init to 0

    for y, row in enumerate(pixels):             #enumerate gives index of an element while iterating hence we get 'y' here for each 'row'
        for x, _ in enumerate(row):
            energy[y][x] = energy_at(pixels, x, y)
    
    return energy


def energy_data_to_colors(energy_data):
    # make the energy image representable (bright means more energy, dull means less energy)

    colors = [[0 for _ in row] for row in energy_data]  #creating 2D array of same size as that of image

    max_energy = max(       #to normalize energy value between 0 to 255
        energy
        for row in energy_data
        for energy in row
    )

    for y, row in enumerate(energy_data):
        for x, energy in enumerate(row):
            energy_normalized = round(energy/max_energy*255)  #normalizing
            colors[y][x] = Color(
                energy_normalized, energy_normalized, energy_normalized  #turing image to greyscale
            )

    return colors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]            #we pass args which are assigned here
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_data_to_colors(energy_data)

    print(f'Saving {output_filename}')
    write_array_into_image(energy_pixels, output_filename)