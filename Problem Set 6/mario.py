while True:
    try:
        height = int(input("Height: "))
        if height >= 1 and height <= 8:
            break
    except ValueError:
        pass


def draw_pyramid(height):
    '''
    composed of spaces, #, spaces, #
    first print right side
    '''
    # for all rows
    for i in range(1, height + 1):
        combined_line = " " * (height - i)
        combined_line += "#" * i
        combined_line += "  "
        combined_line += "#" * i
        print(combined_line)

draw_pyramid(height)