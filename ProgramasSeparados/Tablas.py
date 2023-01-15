from tabulate import tabulate
from bs4 import BeautifulSoup
import requests

with open("mytable.html", 'r') as f:
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

table = list()
row_data = ""
for row in soup.find_all('tr'):
    cells = row.find_all('th')
    if cells:
        row_data = [cell.text for cell in cells]
    else:
        cells = row.find_all('td')
        if cells:
            row_data = [cell.text for cell in cells]
    table.append(row_data)

# table_data = [['Name', 'Age', 'Job'],
#               ['asds', '12', 'Jccob'],
#               ['Namwewee', '56', 'ffd'],
#               ['Nasdame', '34', 'Jzzwsob']]

# Formato SQL
print(tabulate(table, headers='firstrow', tablefmt='psql'))

# Formato sin lineas
# print(tabulate(table_data, headers='firstrow', tablefmt='plain'))

# Formato html
# print(tabulate(table_data, headers='firstrow', tablefmt="html"))

# with open('mytable.html', 'w') as f:
#     f.write(tabulate(table_data, headers='firstrow', tablefmt="html"))

# Crear txt
with open('mytable.txt', 'w') as f:
    f.write(tabulate(table, headers='firstrow', tablefmt="psql"))