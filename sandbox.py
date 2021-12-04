import sys, csv, operator

with open('eiken_3_5.csv') as f:
    reader = csv.reader(f)
    result_row = []
    for row in reader:
        result_row.append([int(row[0]), row[1], row[2]])

result = sorted(result_row, key=operator.itemgetter(0))
print(result)
with open("eiken_3_5.csv", "w") as f:
    data = csv.writer(f, delimiter=',')
    for r in result:
        data.writerow(r)
