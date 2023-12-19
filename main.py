import random

def get_matrix_headers(matrix:list) -> tuple:
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

def is_win(matrix:list, player:str) -> bool:
    """
    Функция проверки победы Игрока/Компьютера.
    """
    return tuple(player*3) in get_matrix_headers(matrix)

def is_valid_matrix(matrix:list) -> bool:
    """
    Функция проверки поля крестики нолики по правилам игры.
    """
    return not (is_win(matrix, 'X') or is_win(matrix, 'O') or abs(matrix.count('X') - matrix.count('O')) >= 2)

def matrix_input() -> list:
    """
    Функция для ввода игрового поля.
    """
    matrix = []
    # Ввод поля при помощи цикла.
    for i in range(3):
        matrix.append(list(input(f"Введите символы X O ? без пробелов в {i+1} строке:\n")))
    print("Полученное поле:\n")
    # Вывод поля при помощи цикла.
    for line in matrix:
        print(*line)
    return matrix

def make_move(matrix:list, player:chr, move:tuple) -> list:
    """
    Функция для выполнения хода на поле.
    """
    i, j = move
    matrix[i][j] = player
    return matrix

def del_move(matrix:list, move:tuple) -> list:
    """
    Функция для отмены хода на поле.
    """
    i, j = move
    matrix[i][j] = '?'
    return matrix

def check_moves(matrix:list) -> list:
    """
    Функция для генерации возможных ходов на поле.
    """
    moves = []
    # Проход по всем клеткам и поиск возможных ходов.
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == '?':
                moves.append((i, j))
    return moves

def find_best_move(matrix:list, player:chr) -> tuple:
    """
    Функция поиска координаты лучшего хода.
    """
    if player == 'X':
        enemy = 'O'
    else:
        enemy = 'X'
    moves = check_moves(matrix)
    # Проверка на возможную победу.
    for move in moves:
        matrix = make_move(matrix, player, move)
        if is_win(matrix, player):
            return move
        matrix = del_move(matrix, move)
    # Проверка на возможный проигрыш.
    for move in moves:
        matrix = make_move(matrix, enemy, move)
        matrix_output(matrix)
        if is_win(matrix, enemy):
            return move
        matrix = del_move(matrix, move)
    # Если мы не смогли найти победу или проигрыш, то делаем рандомный возможных ход.
    return random.choice(check_moves(matrix))

if __name__ == '__main__':
    # Приветствие
    print("""
       Привет Пользователь, я - программа, которая поможет выбрать наиболее оптимальный ход
       при любом раскладке в игре Крестики-Нолики.

       Заполните ПОСТРОЧНО поле формата: 

       ? ? ?
       ? ? ?
       ? ? ?

       Где ? может быть:
       O - Ноль/Нолик/Кружок.
       X - Крест/Крестик/Икс.
       ? - В этом слоте/ячейке/месте на поле ничего не указано.
       """)
    matrix = matrix_input() # Ввод матрицы
    # Проверка поля на верность
    if is_valid_matrix(matrix):
        player = input("\nЗа кого вы играете? O/X (введите один символ): ")
        i, j = find_best_move(matrix, player)
        print("Координаты лучшего хода:", i, j, "\n")
        matrix[i][j] = player
    else:
        print("\nПоле заполнено не по правилам/Игра уже закончилась.\n")
    print("Итоговое поле:\n")
    # Вывод поля
    for line in matrix:
        print(*line)