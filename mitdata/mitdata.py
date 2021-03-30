import csv

with open('1976-2020-senate.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        print(row)
        quit()
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print(f'\t{row["year"]}')
        line_count += 1

    if(line_count == 2):
        quit()
    print(f'Processed {line_count} lines.')
