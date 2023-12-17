# Функция для структурного разбора поля на: Диагонали, строки, поля
def get_matrix_headers(matrix):
    return (
        # ДИАГОНАЛИ
        (matrix[0][0], matrix[1][1], matrix[2][2]), # Главная диагональ
        (matrix[0][2], matrix[1][1], matrix[2][0]), # Побочная диагональ

        # СТРОКИ
        (matrix[0][0], matrix[0][1], matrix[0][2]), # 1 строка
        (matrix[1][0], matrix[1][1], matrix[1][2]), # 2 строка
        (matrix[2][0], matrix[2][1], matrix[2][2]), # 3 строка

        # СТОЛБЦЫ
        (matrix[0][0], matrix[1][0], matrix[2][0]), # 1 столбец
        (matrix[0][1], matrix[1][1], matrix[2][1]), # 2 столбец
        (matrix[0][2], matrix[1][2], matrix[2][2]) # 3 столбец
    )

# Функция для ввода поля
def matrix_input():
    matrix = [] # массив где будет храниться поле
    # Ввод поля при помощи цикла
    for i in range(3):
        # Ввод строки поля и добавление её в массив
        matrix.append(list(input(f"Введите символы [X O ?] без пробелов в {i+1} строке:\n")))

    print("Полученное поле:\n")

    # Вывод поля при помощи цикла
    for line in matrix:
        print(*line)
    print()
    return matrix

# Функция проверки победителя
def is_win(matrix, player):
    if player == 'X':
        STREAK_PL = list("XXX")
        STREAK_AI = list("OOO")
    else:
        STREAK_PL = list("OOO")
        STREAK_AI = list("XXX")

    matrix_headers = get_matrix_headers(matrix)

    if STREAK_AI in matrix_headers:
        return -1 # Победа противника
    elif STREAK_PL in matrix_headers:
        return 1 # Победа игрока
    else:
        return 0 # Нет результата

# Функция генерации массива с возможными ходами
def check_moves(matrix):
    moves = [] # создаем массив, где будут все возможные ходы
    for i in range(3): # проходимся циклом по стобцам
        for j in range(3): # проходимся циклом по строкам
            if matrix[i][j] == '?': # проверяем, свободна ли клетка
                moves.append((i, j)) # добавляем координаты хода на поле в наш массив
    return moves # возвращаем массив с ходами

# Функция выполнения хода
def make_move(matrix, move, player):
    i, j = move
    matrix[i][j] = player

# Функция отмена хода
def undo_move(matrix, move):
    i, j = move # из кортежа вытаскиваем координаты в переменные
    matrix[i][j] = '?' # заменяем X/O на неизвестный обьект

# Функция алгоритма "Нега-Макс"
def negamax(board, depth, maximizing_player, player):
    if depth == 0 or is_win(board, player=player) == (-1 or 1):
        return is_win(board, player=player)

    best_value = float('-inf') if maximizing_player else float('inf')
    moves = check_moves(board)

    for move in moves:
        make_move(board, move, player=player)
        value = -negamax(board, depth - 1, not maximizing_player, player=player)
        undo_move(board, move)

        if maximizing_player:
            best_value = max(best_value, value)
        else:
            best_value = min(best_value, value)
    return best_value

# Функция поиска лучшего хода с помощью Нега-Макса
def find_best_move(board, player):
    best_move = None
    best_value = float('-inf')
    moves = check_moves(board)

    for move in moves:
        make_move(board, move, player=player)
        value = -negamax(board, depth=3, maximizing_player=False, player=player)
        undo_move(board, move)
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

if __name__ == "__main__":
    print("""
    Привет Пользователь, я - программа, которая поможет выбрать наиболее оптимальный ход
    при любом раскладке в игре Крестики-Нолики.

    Заполните поле формата: 

    ? ? ?
    ? ? ?
    ? ? ?

    Где ? может быть:
    O - Ноль/Нолик/Кружок
    X - Крест/Крестик/Икс
    ? - В этом слоте/ячейке/месте на поле ничего не указано
    """)
    matrix = matrix_input()
    player = input("Введи за кого вы играте (СИМВОЛОМ) X/O: ")

    if is_win(matrix, player) != 0:
        print("Невозможно сделать следующий ход")
    else:
        print("Координаты лучшего хода:", *find_best_move(matrix, player), "\n")
        best_i, best_j = find_best_move(matrix, player)
        matrix[best_i][best_j] = player

    print("Итоговое поле:\n")
    for line in matrix:
        print(*line)