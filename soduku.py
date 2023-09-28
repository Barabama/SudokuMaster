import random
import numpy as np


def get_row(sudoku: np.ndarray, row: int) -> np.ndarray:
    """获取格子所在的行的全部格子"""
    return sudoku[row, :]


def get_col(sudoku: np.ndarray, col: int) -> np.ndarray:
    """获取格子所在的列的全部格子"""
    return sudoku[:, col]


def get_block(sudoku: np.ndarray, row: int, col: int) -> np.ndarray:
    """获取格子所在的九宫格的全部格子"""
    row_start = row // 3 * 3
    col_start = col // 3 * 3
    return sudoku[row_start: row_start + 3, col_start: col_start + 3]


def based_sudoku() -> np.ndarray:
    """生成基本盘"""
    # 9*9的二维矩阵, 每个格子默认值为0
    sudoku = np.zeros((9, 9), dtype=int)
    # 随机生成起始的基数(1 ~ 9)
    num = random.randrange(9) + 1

    # 遍历从左到右, 从上到下逐个遍历
    for row_index in range(9):
        for col_index in range(9):
            # 获取该格子对应的行、列、九宫格
            sudoku_row = get_row(sudoku, row_index)
            sudoku_col = get_col(sudoku, col_index)
            sudoku_block = get_block(sudoku, row_index, col_index)

            # 如果该数字已经存在于对应的行、列、九宫格
            # 则继续判断下一个候选数字, 直到没有重复
            while num in sudoku_row or num in sudoku_col or num in sudoku_block:
                num = num % 9 + 1

            # 赋值
            sudoku[row_index, col_index] = num
            num = num % 9 + 1
    return sudoku


def random_sudoku(sudoku: np.ndarray, times=50):
    """随机交换基本盘的行和列"""
    for _ in range(times):
        # 随机交换两行
        rand_row_base = random.randrange(3) * 3  # 从0, 3, 6 随机取一个
        rand_rows = random.sample(range(3), 2)  # 从 0, 1, 2中随机取两个数
        row_1 = rand_row_base + rand_rows[0]
        row_2 = rand_row_base + rand_rows[1]
        sudoku[[row_1, row_2], :] = sudoku[[row_2, row_1], :]

        # 随机交换两列
        rand_col_base = random.randrange(3) * 3
        rand_cols = random.sample(range(3), 2)
        col_1 = rand_col_base + rand_cols[0]
        col_2 = rand_col_base + rand_cols[1]
        sudoku[:, [col_1, col_2]] = sudoku[:, [col_2, col_1]]


def delete_sudoku_nums(sudoku: np.ndarray, del_nums: int) -> np.ndarray:
    """随机擦除数字得到题目"""
    problem = sudoku.copy()

    # 随机擦除（从0到80, 随机取要删除的个数）
    clears = random.sample(range(81), del_nums)
    for clear_index in clears:
        # 把0到80的坐标转化成行和列索引
        # 这样就不会重复删除同一个格子的数字
        row_index = clear_index // 9
        col_index = clear_index % 9
        problem[row_index, col_index] = 0
    return problem


def get_sudoku(level: int, clean_count=(18, 63)) -> list[np.ndarray]:
    """
    编写数独生成算法的代码
    :params level:
    :params clean_count:(最少擦除个数，最大擦除个数)

    """
    # 生成基本盘
    sudoku = based_sudoku()
    # 生成终盘
    random_sudoku(sudoku, 50)

    # 设置难度等级, 0~4, 5个等级：入门、初级、熟练、精通、大神
    level_max = 5
    # 等级范围内的随机系数
    difficulty_factor = random.uniform(level / level_max, (level + 1) / level_max)
    # 擦除的个数
    del_nums = clean_count[0] + int((clean_count[1] - clean_count[0]) * difficulty_factor)

    # 获取数独题目
    problem = delete_sudoku_nums(sudoku, del_nums)

    return [sudoku.tolist(), problem.tolist()]


def show_sudoku(sudoku):
    """打印数独"""
    print("=" * 21)
    for row_index, row in enumerate(sudoku):
        if row_index % 3 == 0 and row_index != 0:
            print("-" * (9 + 8 + 4))
        row.insert(6, "|")
        row.insert(3, "|")
        row_str = " ".join(map(str, row))
        print(row_str.replace("0", " "))
    print("=" * 21)


if __name__ == "__main__":
    sudoku_answer, sudoku_problem = get_sudoku(level=4)
    print("题目：")
    show_sudoku(sudoku_problem)
    print("\n答案：")
    show_sudoku(sudoku_answer)
