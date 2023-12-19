import random

def get_matrix_headers(matrix:list) -> tuple:
    """
    Функция структурного разбора поля на: Диагонали, строки, поля
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
    # Проверяет есть ли комбинация типо OOO или XXX (player * 3) в диагонале/строке/столбце поля.
    return tuple(player * 3) in get_matrix_headers(matrix)

def is_valid_matrix(matrix:list) -> bool:
    """
    Функция проверки поля крестики нолики по правилам игры.
    """
    # Если на поле кто-то победил или разница между символами X/O > 1, то функция посчитает поле не играбельным.
    return not (is_win(matrix, 'X') or is_win(matrix, 'O') or abs(matrix.count('X') - matrix.count('O')) > 1)

def game_result(matrix:list, player:chr) -> str:
    """
    Функция определения результата на поле
    """
    # Определяем игрока и врага.
    if player == 'X':
        enemy = 'O'
    else:
        enemy = 'X'
    # Проходимся по разным условиям, которые соответствуют правилам игры.
    if is_win(matrix, player):
        return f"Выигрыш, победили {player}."
    elif is_win(matrix, enemy):
        return f"Проигрыш, победили {enemy}."
    elif not matrix.count('?'):
        return "Ничья, никто не выбил нужную комбинацию."
    else:
        return "Результата нет, игра продолжается."

def matrix_input() -> list:
    """
    Функция ввода игрового поля.
    """
    matrix = []
    # Ввод поля построчно.
    for i in range(3):
        matrix.append(list(input(f"Введите символы X O ? без пробелов в {i+1} строке:\n")))
    print("Полученное поле:\n")
    # Вывод поля построчно.
    for line in matrix:
        print(*line)
    return matrix

def make_move(matrix:list, player:chr, move:tuple) -> list:
    """
    Функция выполнения хода на поле.
    """
    i, j = move
    matrix[i][j] = player
    return matrix

def del_move(matrix:list, move:tuple) -> list:
    """
    Функция отмены хода на поле.
    """
    i, j = move
    matrix[i][j] = '?'
    return matrix

def check_moves(matrix:list) -> list:
    """
    Функция поиска возможных ходов на поле.
    """
    moves = []
    # Проход по всем клеткам поля и поиск возможных ходов.
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == '?':
                moves.append((i, j))
    return moves

def find_best_move(matrix:list, player:chr) -> tuple:
    """
    Функция поиска координаты лучшего хода.
    """
    # Определяем игрока и врага для дальнешего определения результата.
    if player == 'X':
        enemy = 'O'
    else:
        enemy = 'X'
    moves = check_moves(matrix)
    # Проверки на возможную победу.
    for move in moves:
        matrix = make_move(matrix, player, move)
        if is_win(matrix, player):
            return move
        matrix = del_move(matrix, move)
    # Проверки на возможный проигрыш.
    for move in moves:
        matrix = make_move(matrix, enemy, move)
        if is_win(matrix, enemy):
            return move
        matrix = del_move(matrix, move)
    # Если мы не смогли найти победу или проигрыш, то делаем рандомно один из возможных ходов.
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
    # Ввод матрицы и символа игрока.
    matrix = matrix_input()
    player = input("\nЗа кого вы играете? O/X (введите один символ): ")
    # Проверка поля на верность/конец игры.
    if is_valid_matrix(matrix):
        i, j = find_best_move(matrix, player)
        print("Координаты лучшего хода:", i, j, "\n")
        matrix[i][j] = player
    else:
        print("\nПоле заполнено не по правилам/Игра уже закончилась.\n")
    print("Итоговое поле:\n")
    # Вывод поля и результата на нем.
    for line in matrix:
        print(*line)
    print(f"\nИтог: {game_result(matrix, player)}.")