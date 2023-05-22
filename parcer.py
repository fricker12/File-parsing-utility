import csv
import re
import json

def import_data(file_path, delimiter=',', has_header=True):
    with open(file_path, 'r') as file:
        if delimiter == 'tsv':
            delimiter = '\t'
        elif delimiter == 'dsv':
            delimiter = ';'

        reader = csv.reader(file, delimiter=delimiter)
        data = list(reader)
        if has_header:
            header = data[0]
            data = data[1:]
            return header, data
        else:
            return None, data

def export_data(file_path, data, delimiter=',', header=None):
    with open(file_path, 'w', newline='') as file:
        if delimiter == 'tsv':
            delimiter = '\t'
        elif delimiter == 'dsv':
            delimiter = ';'

        writer = csv.writer(file, delimiter=delimiter)
        if header:
            writer.writerow(header)
        writer.writerows(data)

def filter_data(data, column, value):
    filtered_data = []
    for row in data:
        if row[column] == value:
            filtered_data.append(row)
    return filtered_data

def filter_data_regex(data, column, pattern):
    filtered_data = []
    regex = re.compile(pattern)
    for row in data:
        if regex.search(row[column]):
            filtered_data.append(row)
    return filtered_data

def filter_data_multiple_regex(data, columns, patterns):
    filtered_data = []
    regexes = [re.compile(pattern) for pattern in patterns]
    for row in data:
        if all(regex.search(row[column]) for column, regex in zip(columns, regexes)):
            filtered_data.append(row)
    return filtered_data

def extract_rows(data, ranges):
    extracted_data = []
    for start, end in ranges:
        extracted_data.extend(data[start-1:end])
    return extracted_data

def extract_columns(data, columns):
    extracted_data = []
    for row in data:
        extracted_data.append([row[column] for column in columns])
    return extracted_data

def process_file(file_path):
    try:
        header, data = import_data(file_path)
        # Perform desired operations on the data
        # ...
        # Example: Convert data to JSON
        json_data = json.dumps(data)
        print(json_data)
    except csv.Error as e:
        print(f"CSV format error: {e}")

# Пример использования
file_path = 'example.csv'

# Импорт данных из CSV
header, data = import_data(file_path)

# Фильтрация по значению в определенном поле
filtered_data = filter_data(data, column=2, value='example')

# Фильтрация по регулярному выражению в определенном поле
filtered_data_regex = filter_data_regex(data, column=1, pattern=r'\d{4}')

# Фильтрация по регулярным выражениям в нескольких полях
filtered_data_multiple_regex = filter_data_multiple_regex(data, columns=[0, 2], patterns=[r'example', r'\d{4}'])

# Обработка фрагмента файла: извлечение строк по диапазонам
extracted_rows = extract_rows(data, ranges=[(2, 4), (7, 9)])

# Обработка фрагмента файла: извлечение столбцов
extracted_columns = extract_columns(data, columns=[1, 3, 5])

# Экспорт данных в CSV
export_data('output.csv', data, delimiter=',', header=header)

# Преобразование CSV в JSON
json_data = json.dumps(data)
print(json_data)
