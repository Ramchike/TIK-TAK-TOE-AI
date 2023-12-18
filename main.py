def get_matrix_headers(matrix):
    """
    Функция для структурного разбора поля на: Диагонали, строки, поля
    """
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

def matrix_input():
    """
    Функция для ввода игрового поля
    """
    matrix = [] # массив где будет храниться поле
    # Ввод поля при помощи цикла
    for i in range(3):
        # Ввод строки поля и добавление её в массив
        matrix.append(list(input(f"Введите символы [X O ?] без пробелов в {i+1} строке:\n")))

    print("Полученное поле:\n")

    # Вывод поля при помощи цикла
    for line in matrix:
        print(*line)
    return matrix

def is_win(matrix, player) -> bool:
    """
    Функция проверки победы Игрока/Компьютера

    Ключи возврата:
        Если победил игрок возвращает 1
        Если победил компьютер возвращает -1
        Если в данный момент никто не победил возвращает 0
    """
    if player == 'X':
        STREAK = tuple("XXX")
    else:
        STREAK= tuple("OOO")

    return STREAK in get_matrix_headers(matrix)

def is_full(matrix):
    return '?' not in matrix
def check_moves(matrix):
    """

    :param matrix:
    :return:
    """
    moves = [] # создаем массив, где будут все возможные ходы
    for i in range(3): # проходимся циклом по стобцам
        for j in range(3): # проходимся циклом по строкам
            if matrix[i][j] == '?': # проверяем, свободна ли клетка
                moves.append((i, j)) # добавляем координаты хода на поле в наш массив
    return moves # возвращаем массив с ходами

# Функция выполнения хода
def make_move(matrix, move, player):
    """
    Функция выполнения хода
    """
    i, j = move
    matrix[i][j] = player

# Функция отмена хода
def undo_move(matrix, move):
    """
    Функция отмены хода
    """
    i, j = move # из кортежа вытаскиваем координаты в переменные
    matrix[i][j] = '?' # заменяем X/O на неизвестный обьект

def minimax(matrix, depth, is_maximizing, player):
    if player == 'X':
        ai = '0'
    else:
        ai = 'X'
    scores = {ai: 1, player: -1, 'tie': 0}

    if is_win(matrix, ai):
        return -1
    elif is_win(matrix, player):
        return 1
    elif is_full(matrix):
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for move in get_available_moves(matrix):
            matrix[move] = player
            eval = minimax(matrix, depth + 1, False)
            matrix[move] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in check_moves(matrix):
            matrix[move] = ai
            eval = minimax(matrix, depth + 1, True)
            matrix[move] = ' '
            min_eval = min(min_eval, eval)
        return min_eval


def find_best_move(matrix, player):
    best_move = None
    best_eval = -float('inf')

    for move in check_moves(matrix):
        matrix[move] = player
        eval = minimax(matrix, 2, False, player)
        matrix[move] = ' '

        if eval > best_eval:
            best_eval = eval
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
    """) # Приветствие
    matrix = matrix_input() # Ввод игрового поля
    print(get_matrix_headers(matrix))
    player = input("\nВведи за кого вы играте (СИМВОЛОМ) X/O: ")
    print(is_win(matrix, player))

    if is_win(matrix, player) != 0:
        print("Невозможно сделать следующий ход\n")
    else:
        print("Координаты лучшего хода:", find_best_move(matrix, player), "\n")
        best_i, best_j = find_best_move(matrix, player)
        matrix[best_i][best_j] = player

    print("Итоговое поле:\n")
    for line in matrix:
        print(*line)