# Utils for parsing files

## Requirements

You need the followin to be able to run this code:



## Usage

First install the script and it's requirements:

```
git clone https://github.com/fricker12/File-parsing-utility
cd File-parsing-utility

```
Then run the script as follows:
```
Фильтрация по значению в определенном поле:
python parsing_utils.py input.csv --filter 2 value output.csv
Эта команда фильтрует данные из input.csv по значению 'value' во втором столбце и сохраняет результат в output.csv.

Фильтрация по регулярному выражению в определенном поле:
python parsing_utils.py input.csv --regex-filter 1 pattern output.csv
Эта команда фильтрует данные из input.csv с использованием регулярного выражения 'pattern' (например pattern=r'\d{4}') в первом столбце и сохраняет результат в output.csv.

Фильтрация по регулярным выражениям в нескольких полях:
python parsing_utils.py input.csv --multi-regex-filter 0 pattern1 2 pattern2
Эта команда фильтрует данные из input.csv с использованием регулярных выражений 'pattern1' в нулевом столбце и 'pattern2' (например pattern2 = r'example', r'\d{4}') во втором столбце.

Обработка фрагмента файла: извлечение строк по диапазонам:
python parsing_utils.py input.csv --extract-rows 2 4 7 9
Эта команда извлекает строки из input.csv с 2 по 4 и с 7 по 9 (включительно) и выводит результат на экран.

Обработка фрагмента файла: извлечение столбцов:
python parsing_utils.py input.csv --extract-columns 1 3 5
Эта команда извлекает столбцы 1, 3 и 5 из input.csv и выводит результат на экран.

Экспорт данных в CSV:
python parsing_utils.py input.csv --export output.csv
Эта команда экспортирует данные из input.csv в output.csv.

Преобразование CSV в JSON:
python parsing_utils.py input.csv
Эта команда преобразует данные из input.csv в формат JSON и выводит результат на экран.

Получение данных одного поля в формате одиночной строки:
python parsing_utils.py --get-field-data 2 single
В этом примере мы получаем данные из столбца номер 2 в формате одиночной строки. Результат будет выведен на экран.

Получение данных одного поля в формате множества строк:
python parsing_utils.py --get-field-data 3 multi
Здесь мы получаем данные из столбца номер 3  в формате множества строк. Результат будет выведен на экран.






