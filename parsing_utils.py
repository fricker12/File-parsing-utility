import csv
import re
import json
import argparse
  
# При возникновении ошибки канонического формата CSV файла, скрипт будет выводить сообщение об ошибке и попытается получить содержимое файла в виде списка строк file_content.       
def import_data(file_path, delimiter=',', has_header=True):
    try:
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
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None, None
    except csv.Error as e:
        print(f"CSV format error: {e}")
        file_content = []
        with open(file_path, 'r') as file:
            file_content = file.readlines()
        return None, file_content

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

def extract_rows(data, ranges, join_rows=False):
    extracted_data = []
    for start, end in ranges:
        extracted_data.extend(data[start-1:end])
    if join_rows:
        return [' '.join(row) for row in extracted_data]
    else:
        return extracted_data
    
def get_field_data(data, column, join=False):
    field_data = [row[column] for row in data]
    if join:
        return ' '.join(field_data)
    else:
        return field_data

def extract_columns(data, columns):
    extracted_data = []
    for row in data:
        extracted_data.append([row[column] for column in columns])
    return extracted_data

def process_file(file_path):
    try:
        header, data = import_data(file_path)
        json_data = json.dumps(data)
        print(json_data)
    except csv.Error as e:
        print(f"CSV format error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Utils for parsing files')
    parser.add_argument('file_path', help='Path to the CSV file')
    parser.add_argument('--delimiter', choices=['comma', 'tab', 'semicolon'], default='comma',
                        help='Delimiter used in the CSV file (default: comma)')
    parser.add_argument('--header', action='store_true', help='Specify if the CSV file has a header row')
    parser.add_argument('--filter', nargs=3, metavar=('column', 'value', 'output_file'),
                        help='Filter data by a specific value in a column and save the result to a file')
    parser.add_argument('--regex-filter', nargs=3, metavar=('column', 'pattern', 'output_file'),
                        help='Filter data by a regular expression pattern in a column and save the result to a file')
    parser.add_argument('--multi-regex-filter', nargs='*', metavar=('column', 'pattern'),
                        help='Filter data by multiple regular expression patterns in multiple columns')
    parser.add_argument('--extract-rows', nargs='+', type=int, metavar=('start', 'end'),
                        help='Extract rows from the specified start to end indices and print the result')
    parser.add_argument('--extract-columns', nargs='+', type=int, metavar='column',
                        help='Extract specified columns and print the result')
    parser.add_argument('--export', metavar='output_file', help='Export data to a CSV file')
    parser.add_argument('--get-field-data', nargs=2, metavar=('column', 'format'),
                        help='Get data from a specific column in the chosen format (single/multi-string)')

    args = parser.parse_args()

    file_path = args.file_path
    delimiter = ','
    if args.delimiter == 'tab':
        delimiter = 'tsv'
    elif args.delimiter == 'semicolon':
        delimiter = 'dsv'
    has_header = args.header

    header, data = import_data(file_path, delimiter=delimiter, has_header=has_header)

    if args.filter:
        column, value, output_file = args.filter
        # Фильтрация по значению в определенном поле
        filtered_data = filter_data(data, int(column), value)
        export_data(output_file, filtered_data, delimiter=delimiter, header=header)
    
    if args.regex_filter:
        column, pattern, output_file = args.regex_filter
        # Фильтрация по регулярному выражению в определенном поле
        filtered_data_regex = filter_data_regex(data, int(column), pattern)
        export_data(output_file, filtered_data_regex, delimiter=delimiter, header=header)

    if args.multi_regex_filter:
        columns = [int(column) for column in args.multi_regex_filter[::2]]
        patterns = args.multi_regex_filter[1::2]
        # Фильтрация по регулярным выражениям в нескольких полях
        filtered_data_multiple_regex = filter_data_multiple_regex(data, columns, patterns)
        export_data('output.csv', filtered_data_multiple_regex, delimiter=delimiter, header=header)
    
    if args.extract_rows:
        ranges = [(start, end) for start, end in zip(args.extract_rows[::2], args.extract_rows[1::2])]
        extracted_rows = extract_rows(data, ranges, join_rows=True)
        print(extracted_rows)
    
    
    if args.extract_columns:
        # Обработка фрагмента файла: извлечение столбцов
        extracted_columns = extract_columns(data, args.extract_columns)
        print(extracted_columns)

    if args.export:
        # Экспорт данных в CSV
        export_data(args.export, data, delimiter=delimiter, header=header)
        
     # Получения данных полей в формате одиночной строки (--get-field-data <column> single) или множества строк (--get-field-data <column> multi).  
    if args.get_field_data:
        column, format = args.get_field_data
        if format == 'single':
            field_data = get_field_data(data, int(column), join=True)
            print(field_data)
        elif format == 'multi':
            field_data = get_field_data(data, int(column), join=False)
            print(field_data)
        else:
            print("Invalid format. Please choose 'single' or 'multi'.")

    # Преобразование CSV в JSON
    json_data = json.dumps(data)
    print(json_data)

if __name__ == '__main__':
    main()
