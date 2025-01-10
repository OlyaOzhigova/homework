# -*- coding: utf-8 -*-
import functools
import logging
# Логирование будет для домашнего задания к лекции «Открытие и чтение файла, запись в файл» для задачи 3
def parameterized_logger(log_path):
    def logger_decorator(func):
        logging.basicConfig(level=logging.INFO, filename=log_path, filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logging.info(f"Function '{func.__name__}' called with args={args}, kwargs={kwargs}, returned {result}")
            return result

        return wrapper

    return logger_decorator


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.readlines()


@parameterized_logger('write_result_file_log.txt')
def write_result_file(file_data, result_file_name):
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for file_name, lines in file_data:
            result_file.write(f"{file_name}\n{len(lines)}\n")
            result_file.writelines(lines)
            result_file.write("\n")  # пустая строка


def main():
    file_names = ["3.3_1.txt", "3.3_2.txt"]

    file_data = [(file_name, read_file(file_name)) for file_name in file_names]

    file_data.sort(key=lambda x: len(x[1]))
    print("сортировка", file_data)

    write_result_file(file_data, "result.txt")


if __name__ == "__main__":
    main()