# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from ExcelReader import read_excel
from Strapi import strapi_classes
from widgetCreation import create_widget

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = '/Users/changdeojadhav/Downloads/widgets.xlsx'
    sheet_name = 'Example Class'
    accessToken = f'Bearer'  # f'Bearer {Your AccessToken}'

    data = read_excel(file_path, sheet_name)
    classes = strapi_classes('aol-org')

    if data:
        for row in data:
            classTemp = int(row.get('ClassId', None))
            programID = classes.get(classTemp, None)

            if classTemp is not None and programID is not None:
                print(classes[classTemp])
                create_widget(row['Widget Type'], row, programID)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
