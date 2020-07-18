from os import path
from image_io import *
from image_operation import *


valid_commands = {'--rotate', '--mirror', '--inverse', '--bw', '--lighten', '--darken', '--sharpen', '--blur'}

# Commands expected to have a value after them
commands_with_value = {'--lighten', '--darken'}

help_message = 'Usage: python graphic_editor.py [OPERATION]... [INPUT_FILE] [OUTPUT_FILE] \n\n' \
               'Apply OPERATIONs on the INPUT_FILE and write result to OUTPUT_FILE \n' \
               '--rotate                        Rotate an image 90 degrees to the right\n' \
               '--mirror                        Mirrored image \n' \
               '--inverse                       Inverse image  \n' \
               '--bw                            Transform to black and white \n' \
               '--lighten <percentage: 0-100>   Make image some percentage lighter \n' \
               '--darken <percentage: 0-100>    Make image some percentage darker \n' \
               '--sharpen                       Apply sharpening kernel on the image \n' \
               '--blur                          Apply Gaussian blur 3x3 \n' \
               '<INPUT_FILE>                    Path to the input file \n' \
               '<OUTPUT_FILE>                   Path to the output file \n'


# Runs validation on the arguments and then applies them
def apply_args(args):
    args_len = len(args)
    if args_len == 2 and args[1] == '--help':
        print_help_msg()
        return

    validate_args(args)

    # Last two are image paths
    input_file = args[args_len - 2]
    output_file = args[args_len - 1]

    image = read_image(input_file)
    mode = 'L' if image.ndim == 2 else 'RGB'

    prev_arg = ''
    # Apply arguments on the input_file
    for i in range(1, args_len - 2):
        if args[i] in commands_with_value:
            prev_arg = args[i]
            continue
        if args[i].isdigit():
            image, mode = apply_arg(image, prev_arg, args[i], mode)
            continue

        image, mode = apply_arg(image, args[i], mode=mode)

    # Done, save result
    save_image(image, output_file, mode)


# Applies the given operation on the image and returns image after the operation
def apply_arg(image_arr: np.array, op, value=None, mode='RGB') -> np.array:
    if op == '--rotate':
        image_arr = rotate(image_arr)
    elif op == '--mirror':
        image_arr = flip(image_arr)
    elif op == '--inverse':
        image_arr = inverse(image_arr)
    elif op == '--bw':
        image_arr = get_bw(image_arr)
        mode = 'L'
    elif op == '--lighten':
        image_arr = adjust_gamma(image_arr, int(value))
    elif op == '--darken':
        image_arr = adjust_gamma(image_arr, int(value) * -1)
    elif op == '--sharpen':
        image_arr = apply_filter(image_arr, sharpening_kernel)
    elif op == '--blur':
        image_arr = apply_filter(image_arr, approx_gaussian_blur_3_kernel)

    return image_arr, mode


# Validates that arguments follow the required format and throws exception if not
def validate_args(args):
    args_len = len(args)
    if args_len < 3:
        raise Exception('Not enough arguments provided')

    prev_arg = ''
    # Skip first argument, being the path to the executed file
    for i in range(1, args_len - 2):
        if args[i].isdigit() and prev_arg in commands_with_value:
            continue

        if is_valid(args[i]):
            if args[i] in commands_with_value:
                prev_arg = args[i]
        else:
            raise Exception('Invalid argument: {}'.format(args[i]))

    # Check that input file exists
    if path.exists(args[args_len - 2]) is False:
        raise Exception('Input file does not exist')


# Checks whether argument is within the accepted arguments
def is_valid(arg) -> bool:
    return arg in valid_commands


# Print help message
def print_help_msg():
    print(help_message)
