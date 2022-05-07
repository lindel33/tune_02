import csv

headers = [
    'Id',
    'AvitoId',
    'AdStatus',
    'Category',
    'GoodsType',
    'Address',
    'Title',
    'Description',
    'Condition',
    'Price',
    'DateBegin',
    'DateEnd',
    'AllowEmail',
    'ManagerName',
    'ContactPhone',
    'Brand',
    'Model',
    'Color',
    'MemorySize',
    'RamSize',
    'ImageUrls'
           ]



def new_avito(data_new):
    with open('C:\\Users\\luky\\PycharmProjects\\tune\\avito.csv', 'a', encoding='utf-8') as f:
        data = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        data.writeheader()
        data.writerow(data_new)