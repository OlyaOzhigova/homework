# -*- coding: utf-8 -*-

# открытие и чтение
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.readlines()


def write_result_file(file_data, result_file_name):
    # объединить в 1
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for file_name, lines in file_data:
            # print("№ файла:", file_name)
            # print("длина:", len(lines))
            result_file.write(f"{file_name}\n{len(lines)}\n")
            result_file.writelines(lines)
            result_file.write("\n")  # пустая строка

def main():
    # файлф на вход
    file_names = ["1.txt", "2.txt"]
    # file_data = ([])
    # for file_name in file_names:
    #     file_data.append(file_name)
    #     file_data.append(read_file(file_name))
    #     for i in range(1, len(file_data), 2):
    #         # Сортируем список строк по длине
    #         file_data[i].sort(key=len)
    #         print("file_data_0", file_data)

    #     # отсортировать
    #     for i in range(0, len(file_data), 2):
    #         print(f"Файл: {file_data[i]}")
    #         for line in file_data[i + 1]:
    #             print("line: ", line)

    file_data = [(file_name, read_file(file_name)) for file_name in file_names]
    # print("до сортировки", file_data)

    # Сортируем по длине
    file_data.sort(key=lambda x: len(x[1]))
    print("сортировка", file_data)

    # создать новый файл с нужным выводом
    write_result_file(file_data, "result.txt")


if __name__ == "__main__":
    main()