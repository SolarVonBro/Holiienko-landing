import re
from collections import Counter


def read_text_from_file(file_path):
    """
    Читает текст из файла.

    :param file_path: путь к текстовому файлу
    :return: строка с содержимым файла или None при ошибке
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Ошибка: файл не найден.")
        return None
    except UnicodeDecodeError:
        print("Ошибка: не удалось прочитать файл. Проверьте кодировку.")
        return None


def input_text_manually():
    """
    Позволяет пользователю ввести текст вручную.
    Ввод завершается пустой строкой.

    :return: введённый пользователем текст
    """
    print("Введите текст для анализа.")
    print("Для завершения ввода нажмите Enter на пустой строке.")

    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines)


def get_words(text):
    """
    Извлекает слова из текста.

    Используется регулярное выражение, которое выделяет русские,
    английские слова и числа. Все слова приводятся к нижнему регистру.

    :param text: исходный текст
    :return: список слов
    """
    return re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", text.lower())


def count_sentences(text):
    """
    Подсчитывает количество предложений в тексте.

    Предложение определяется по наличию символов '.', '!' или '?'.
    Такой подход является упрощённым, но подходит для учебного проекта.

    :param text: исходный текст
    :return: количество предложений
    """
    sentences = re.findall(r"[.!?]+", text)
    return len(sentences)


def analyze_text(text, top_n=5):
    """
    Анализирует текст и возвращает основные статистические показатели.

    :param text: исходный текст
    :param top_n: количество наиболее частотных слов для вывода
    :return: словарь с результатами анализа
    """
    words = get_words(text)
    word_counter = Counter(words)

    result = {
        "characters_with_spaces": len(text),
        "characters_without_spaces": len(text.replace(" ", "").replace("\n", "")),
        "words_count": len(words),
        "sentences_count": count_sentences(text),
        "top_words": word_counter.most_common(top_n)
    }

    return result


def print_analysis_result(result):
    """
    Выводит результаты анализа текста в консоль.

    :param result: словарь с результатами анализа
    """
    print("\nРезультаты анализа текста:")
    print("-" * 40)
    print(f"Количество символов с пробелами: {result['characters_with_spaces']}")
    print(f"Количество символов без пробелов: {result['characters_without_spaces']}")
    print(f"Количество слов: {result['words_count']}")
    print(f"Количество предложений: {result['sentences_count']}")

    print("\nНаиболее часто встречающиеся слова:")
    if result["top_words"]:
        for word, count in result["top_words"]:
            print(f"{word}: {count}")
    else:
        print("Слова не найдены.")


def main():
    """
    Главная функция программы.

    Предлагает пользователю выбрать способ ввода текста:
    1. Ввод вручную.
    2. Чтение из файла.
    """
    print("Консольная программа анализа текста")
    print("=" * 40)
    print("Выберите способ ввода текста:")
    print("1 — Ввести текст вручную")
    print("2 — Прочитать текст из файла")

    choice = input("Ваш выбор: ")

    if choice == "1":
        text = input_text_manually()
    elif choice == "2":
        file_path = input("Введите путь к файлу: ")
        text = read_text_from_file(file_path)

        if text is None:
            return
    else:
        print("Ошибка: выбран неверный пункт меню.")
        return

    if not text.strip():
        print("Ошибка: текст пустой.")
        return

    result = analyze_text(text)
    print_analysis_result(result)


if __name__ == "__main__":
    main()