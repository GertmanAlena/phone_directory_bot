def correct_name():
    """Проверка правильности ввода имени"""
    while True:
        name = input("Введите имя-> ")
        if name.isalpha() and len(name) < 10:
            return name.capitalize()
        else:
            # logger.data_name("Введено не корректное имя или фамилия.")
            print("\033[31m {}\033[0m" .format("Введены не корректные данные"))
            