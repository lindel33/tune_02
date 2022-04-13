# import re
# from pprint import pprint
from django.db import models
from price.models import Global, Iphone, Markup, Ipad
from .service import get_product_list
from .startsvc import get_cvs_data, new_cvs_data

mega_count = []


class ProviderModel(models.Model):
    name = models.CharField('Имя', max_length=20)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщик'

    def __str__(self):
        return self.name


class DetailModel(models.Model):
    device = models.CharField('Устройство', max_length=30)
    series = models.CharField('Серия', max_length=30)
    memory = models.CharField('Память', max_length=30)
    cost = models.CharField('Цена', max_length=30)
    color = models.CharField('Цвет', max_length=30)
    region = models.CharField('Регион', max_length=30)
    extra = models.CharField('Исходная строка', max_length=255)
    new_line = models.CharField('Строка состояния', max_length=255)
    provider = models.CharField('Поставщик', max_length=25)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Цены | Поиск'
        verbose_name_plural = 'Цены | Поиск'

    def __str__(self):
        return self.device


class NewPriceModel(models.Model):
    provider = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name='Поставщик')
    price = models.TextField('Новый прайс')
    csv_file = get_cvs_data()
    csv_file_copy = csv_file.copy()
    id_products = []
    new_products = []

    class Meta:
        verbose_name = 'Новый прайс | Управление cvs файлом'
        verbose_name_plural = 'Новый прайс | Управление cvs файлом'

    def __str__(self):
        return self.provider.name

    def save(self, *args, **kwargs):
        list_new_products = get_product_list(self.price)
        zzz = 0
        for product in list_new_products:
            DetailModel.objects.create(
                device=product['device'],
                series=product['series'],
                memory=product['memory'],
                cost=product['cost'],
                color=product['color'],
                region=product['region'],
                extra=product['extra'],
                provider=self.provider.name,
                new_line=str(product['device']) + ' ' +
                         str(product['series']) + ' ' +
                         str(product['memory']) + ' ' +
                         str(product['color']) + ' ' +
                         str(product['region']) + ' ' +
                         str(product['cost'])
            )
            next_product = self._get_csv_product(product)  # обновленные товары что есть в прайсе

            if next_product:
                self.new_products.append(next_product)
                zzz += 1
        self.set_new_price_on_grope(self.id_products)

        new_cvs_data(self.new_products)
        self.new_products = []
        # for i in self.csv_file:
        #     if 'Yellow' in i['Title']:
        #         print(i['Title'])
        super().save(*args, **kwargs)

    def _get_csv_product(self, product):
        """
        Поиск всех товаров в csv_file которые есть в свежем прайсе
        :param product:
        :return:
        """
        device = product['device'].lower()
        series = product['series'].lower()
        color = product['color'].lower()
        memory = self.get_memory(product['memory'].lower())
        memory_extra = '64|128|256|512'
        series = re.sub(memory_extra, '', series.lower())
        # series = self.get_series(series)
        series = series.replace(' ', '')
        if memory == '1':
            memory = 'тб'
        for line in self.csv_file:
            title = line['Title'].lower().replace(' ', '')
            editions = line['Editions'].lower().replace(' ', '')

            if device in title or device in editions:
                if (series.replace(' ', '') + ',' in title.replace(' ', '') or
                    series.replace(' ', '') + ';' in editions.replace(' ', '')) \
                        and device != 'macbook':
                    if color in title or color in editions:
                        if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                            self.csv_file.remove(line)
                            line['Price'] = self.new_cost(current_cost=line['Price'],
                                                          price_cost=product['cost'],
                                                          device=product['device'])

                            self.id_products.append({
                                'device': device,
                                'series': series,
                                'color': color,
                                'memory': memory,
                                'Tilda UID': line['Tilda UID'],
                                'cost': line['Price'],
                                'Title': line['Title']})

                            return line

                elif device == 'macbook':
                    if (series.replace(' ', '') in title.replace(' ', '') or
                            series.replace(' ', '') in editions.replace(' ', '')):
                        if color in title or color in editions:

                            if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                                self.csv_file.remove(line)
                                line['Price'] = self.new_cost(current_cost=line['Price'],
                                                              price_cost=product['cost'],
                                                              device=product['device'])

                                self.id_products.append({
                                    'device': device,
                                    'series': series,
                                    'color': color,
                                    'memory': memory,
                                    'Tilda UID': line['Tilda UID'],
                                    'cost': line['Price'],
                                    'Title': line['Title']})
                                return line

    @staticmethod
    def new_cost(current_cost, price_cost, device) -> str:
        markup = Markup.objects.get(name_models=f'{device.replace(" ", "")}')
        if float(str(current_cost)) < float(str(price_cost)):
            if markup.flag:
                new_cost = float(price_cost) + (float(price_cost) * markup.markup / 100)
                exit_cost = [x for x in str(int(new_cost))]
                exit_cost[-3], exit_cost[-2], exit_cost[-1] = '9', '9', '0'
                return str(int("".join(exit_cost)))
            if not markup.flag:
                return str(float(price_cost) + float(markup.markup_int))
        else:
            return str(float(price_cost) + float(markup.markup_int))

    def set_new_price_on_grope(self, product_list):
        """
        Вернет товар который не найден в _get_csv_product по uid
        Для выставления цены на группу товаров
        Два пробега работает? :|
        :param product_list:
        :return:
        """
        c = 0
        print('Длинна ло неГруппы', len(self.csv_file))
        clear_list = self.get_clear_list(product_list)
        count = self.get_products_len(clear_list) + len(self.new_products)
        while len(self.new_products) != count:
            print(len(self.new_products), count)
            for product in clear_list:
                device = product['device'].lower()
                series = product['series'].lower()
                color = product['color'].lower()
                memory = product['memory'].lower()
                if memory == '1':
                    memory = 'тб'
                for line in self.csv_file:
                    title = line['Title'].lower()
                    editions = line['Editions'].lower()

                    if device in title or device in editions:
                        if series.replace(' ', '') + ',' in title.replace(' ', '') or \
                                series.replace(' ', '') + ';' in editions.replace(' ', ''):

                            if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                                self.csv_file.remove(line)
                                line['Price'] = product['cost']
                                self.new_products.append(line)


    def get_memory(self, memory):
        new_memory = memory.replace(' ', '')
        prefix_memory = 'гб|gb|тр|tb'
        if re.findall(prefix_memory, new_memory.lower()):
            new_memory = re.sub(prefix_memory, '', new_memory.lower())
            new_memory = new_memory.replace(' ', '')
            
        return new_memory

    def get_series(self, series):
        if len(series.split()) > 1:
            new_series = series.split()[1]
            return new_series
        if len(series.split()) == 1:
            new_series = series
            return new_series
        return 'Series not search'

    def get_clear_list(self, products):
        series = []
        series_cost = []
        for product in products:
            product['extra_series'] = product['series'] + product['memory']
            if product['extra_series'] not in series:
                series.append(product['extra_series'])
        for i in list(set(series)):
            tmp_cost = '0'
            series_tmp = ''
            for j in products:
                if i == j['extra_series']:

                    series_tmp = j
                    products.remove(j)
                    if j['cost'] > tmp_cost:
                        tmp_cost = j['cost']

            series_tmp['cost'] = tmp_cost
            series_cost.append(series_tmp)

        # pprint(series_cost)
        return series_cost


    def get_products_len(self, products):
        count = 0
        for product in products:
            device = product['device'].lower()
            series = product['series'].lower()
            memory = product['memory'].lower()
            if memory == '1':
                memory = 'тб'
            for line in self.csv_file:
                title = line['Title'].lower()
                editions = line['Editions'].lower()
                if device in title or device in editions:
                    if series.replace(' ', '') + ',' in title.replace(' ', '') or \
                            series.replace(' ', '') + ';' in editions.replace(' ', ''):

                        if memory in title.replace(' ', '') or memory in editions.replace(' ', ''):
                            count += 1
        return count
