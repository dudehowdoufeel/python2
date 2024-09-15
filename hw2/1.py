def letterO():
    rows = 7
    cols = 5
    
    for i in range(rows):
        for j in range(cols):
            if (i == 0 or i == rows - 1 or j == 0 or j == cols - 1) and not (i in [0, rows - 1] and j in [0, cols - 1]):
                print('*', end='')
            else:
                print(' ', end='')
        print()

letterO()
