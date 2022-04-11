# Generated by Django 4.0.3 on 2022-04-10 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tune_admin.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tune_admin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_1', models.ImageField(upload_to='', verbose_name='Картинка 1')),
                ('image_2', models.ImageField(upload_to='', verbose_name='Картинка 2')),
                ('image_3', models.ImageField(blank=True, upload_to='', verbose_name='Картинка 3')),
                ('sell', models.BooleanField(default=False, verbose_name='Продано?')),
                ('booking', models.BooleanField(default=False, verbose_name='Забронированно?')),
                ('moderation', models.BooleanField(default=False, verbose_name='Допущен к публикации?')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('smile', models.CharField(blank=True, choices=[('🔥', '🔥'), ('💥', '💥'), ('⚡', '⚡'), ('₽', '₽')], default='₽', help_text='Оставить пустым, если не нужен', max_length=5, null=True, verbose_name='Эмодзи к цене')),
                ('name', models.CharField(help_text='Пример: iPhone 7 128 Blue ||Формат: Модель/ Серия/ (Память/ Цвет/ Регион)-> если есть \n ', max_length=150, verbose_name='Название')),
                ('name_tmp', models.CharField(max_length=50, verbose_name='Фоновое имя')),
                ('tests', models.BooleanField(default=False, verbose_name='Ростест?')),
                ('article', models.CharField(help_text='Пример: 20X100ZT', max_length=15, verbose_name='Код товара')),
                ('state', models.TextField(choices=[('Новое устройство, вскрыта упаковка. Не активировано.', 'Новый'), ('Новое устройство, выдано по гарантии взамен неисправному устройству в авторизованном сервисном центре (АСЦ) Apple. Абсолютно новое, не активированное.', 'Обменка'), ('Устройство в идеальном состоянии. Полностью работоспособно. Не имеет царапин и потертостей на корпусе и дисплее.', 'Как новый'), ('Устройство в отличном состоянии. Полностью работоспособно. На корпусе и/ или дисплее минимальные царапины и потертости. Без проблем закроются премиум защитным стеклом/чехлом.', 'Отличное'), ('Устройство в хорошем состоянии. Полностью работоспособно. На корпусе и/ или дисплее есть царапины и потертости. Без проблем закроются премиум защитным стеклом/чехлом.', 'Хорошее ')], help_text='Выбор сгенерирует шаблон', verbose_name='Состояние')),
                ('state_akb', models.SmallIntegerField(default=0, help_text='Оставить в поле 0, если по АКБ нет информации', verbose_name='Состояние АКБ')),
                ('works', models.TextField(blank=True, help_text='Оставить поле пустым, если не нужно', null=True, verbose_name='Произведенные работы')),
                ('kit', models.CharField(choices=[('Без комплекта', 'Только устройство'), ('Коробка', 'Коробка'), ('Коробка, кабель Lightning — USB-C для быстрой зарядки', 'Коробка, кабель Lightning — USB-C для быстрой зарядки'), ('Кабель Lightning — USB-C для быстрой зарядки', 'Кабель Lightning — USB-C для быстрой зарядки'), ('Коробка, кабель Lightning — USB для зарядки', 'Коробка, кабель Lightning — USB для зарядки'), ('Только часы', 'Только часы'), ('Часы + зарядное устройство ', 'Часы + зарядное устройство '), ('Кабель USB‑C для быстрой зарядки Apple Watch ', 'Кабель USB‑C для быстрой зарядки Apple Watch '), ('Кабель USB для зарядки Apple Watch', 'Кабель USB для зарядки Apple Watch'), ('Полный', 'Полный')], max_length=150, verbose_name='Комплект')),
                ('guaranty', models.CharField(blank=True, choices=[('Гарантия от магазина на проверку 3 месяца!✅', 'Гарантия от магазина на проверку 3 месяца!✅'), ('Официальная гарантия Apple 2 года!✅', 'Официальная гарантия Apple 2 года!✅'), ('Официальная гарантия Apple 1 год!✅', 'Официальная гарантия Apple 1 год!✅')], default='Гарантия от магазина на проверку 3 месяца !✅', max_length=255, null=True, verbose_name='Гарантия')),
                ('custom_guaranty', models.DateField(blank=True, null=True, verbose_name='Своя гарантия')),
                ('base_text', models.TextField(default='Доступен trade-in ♻️\n(Сдаете старое устройство - получаете скидку на новое)\n\nСамовывоз - СПБ, ул. Восстания 7, БЦ «Андреевский», офис 208\n\nОтправляем доставкой по всей России 🇷🇺 транспортной компанией «СДЕК» 📦\n\n', verbose_name='Нижняя подпись к посту')),
                ('day_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('day_next_publish', models.DateTimeField(default=tune_admin.models.get_deadline, verbose_name='Дата следующего поста')),
                ('count', models.SmallIntegerField(default=0, verbose_name='Счетчик сохранений')),
                ('up_price', models.BooleanField(default=False, verbose_name='Цена поднята?')),
                ('provider_device', models.CharField(choices=[('Устройсво клиента', 'Устройсво клиента'), ('Илья Савичев', 'Илья Савичев'), ('Эмиль', 'Эмиль')], default='Устройсво клиента', max_length=50, verbose_name='Поставщик')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tune_admin.category', verbose_name='Модель')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tune_admin.seriescategory', verbose_name='Серия')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
    ]