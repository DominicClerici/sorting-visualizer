import pygame
import random
import math

pygame.init()


class DrawInformation:
    BUTTON_DEF = 150, 150, 150
    BUTTON_CLICK = 100, 100, 100
    BUTTON_ACTIVE = 50, 50, 50
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0

    BACKGROUND_COLOR = WHITE

    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]

    BUTTONFONT = pygame.font.SysFont("Courier New", 16)
    FONT = pygame.font.SysFont("Courier New", 20)
    LARGE_FONT = pygame.font.SysFont("Courier New", 30)
    SIDE_PAD = 100

    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        )
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, sorting, ascending, sorting_algo_index):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    sorting_algo_names = ["Insertion sort", "Bubble sort", "Selection sort", "Shell sort"]

    reset = draw_info.FONT.render(
        "R - Reset.", True, draw_info.BLACK
    )
    draw_info.window.blit(
        reset, (10, 10)
    )
    startStop = draw_info.FONT.render(
        "Space - Start/stop sorting.", True, draw_info.BLACK
    )
    draw_info.window.blit(
        startStop, (10, 30)
    )

    asc = draw_info.FONT.render(
        "Up Arrow - Ascending", True, draw_info.RED if ascending else draw_info.BLACK
    )
    draw_info.window.blit(
        asc, (draw_info.width - asc.get_width() - 10, 10)
    )

    desc = draw_info.FONT.render(
        "Down Arrow - Descending", True, draw_info.RED if not ascending else draw_info.BLACK
    )
    draw_info.window.blit(
        desc, (draw_info.width - desc.get_width() - 10, 30)
    )

    sorting = draw_info.FONT.render(
       "Left/right arrow key - Change algorithm", True, draw_info.BLACK
    )
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 70))
    currentAlgo = draw_info.FONT.render(
       f"Current algorithm: {sorting_algo_names[sorting_algo_index]}", True, draw_info.BLACK
    )
    draw_info.window.blit(currentAlgo, (draw_info.width / 2 - currentAlgo.get_width() / 2, 90))

    draw_list(draw_info)


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)
        )
    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    arr = draw_info.lst
    n = len(arr)
    if ascending:
        for i in range(1, n):
            
            key = arr[i]

            j = i-1
            while j >=0 and key < arr[j] :
                    arr[j+1] = arr[j]
                    j -= 1
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True
            arr[j+1] = key
    else:
        for i in range(1, n):
            
            key = arr[i]

            j = i-1
            while j >=0 and key > arr[j] :
                    arr[j+1] = arr[j]
                    j -= 1
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True
            arr[j+1] = key

def shell_sort(draw_info, ascending=True):

    arr = draw_info.lst
    list_len = len(arr)
    interval = list_len // 2
    if ascending:
        while interval > 0:
            for i in range(interval, list_len):
                temp = arr[i]
                j = i
                while j >= interval and arr[j - interval] > temp:
                    arr[j] = arr[j - interval]
                    j -= interval
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True
                arr[j] = temp
            interval //= 2
    else: 
        while interval > 0:
            for i in range(interval, list_len):
                temp = arr[i]
                j = i
                while j >= interval and arr[j - interval] < temp:
                    arr[j] = arr[j - interval]
                    j -= interval
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True
                arr[j] = temp
            interval //= 2

def selection_sort(draw_info, ascending=True):
    array = draw_info.lst
    size = len(array)
    if ascending:
        for ind in range(size):
            min_index = ind
    
            for j in range(ind + 1, size):
                if array[j] < array[min_index]:
                    min_index = j
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
            (array[ind], array[min_index]) = (array[min_index], array[ind])
    else:
        for ind in range(size):
            min_index = ind
    
            for j in range(ind + 1, size):
                if array[j] > array[min_index]:
                    min_index = j
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
            (array[ind], array[min_index]) = (array[min_index], array[ind])


def main():
    run = True
    sorting = False
    ascending = True
    clock = pygame.time.Clock()

    sorting_algo_index = 0

    sorting_algos = [insertion_sort, bubble_sort, selection_sort, shell_sort]

    sorting_algo_generator = None

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False

        draw(draw_info, sorting, ascending, sorting_algo_index)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE:
                    sorting = not sorting
                    sorting_algo_generator = sorting_algos[sorting_algo_index](draw_info, ascending)
                elif event.key == pygame.K_UP and not sorting:
                    ascending = True
                elif event.key == pygame.K_DOWN and not sorting:
                    ascending = False
                elif event.key == pygame.K_RIGHT and not sorting:
                    sorting_algo_index = (sorting_algo_index + 1) % len(sorting_algos) 
                    print(sorting_algo_index)
                elif event.key == pygame.K_LEFT and not sorting:
                    sorting_algo_index = (sorting_algo_index - 1) % len(sorting_algos) 
                    print(sorting_algo_index)
    pygame.quit()


if __name__ == "__main__":
    main()
