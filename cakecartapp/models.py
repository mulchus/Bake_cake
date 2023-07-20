from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Form(models.Model):
    name = models.CharField('Название',
                            max_length=200,)
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.name}: {self.price} р.'


class Topping(models.Model):
    name = models.CharField('Название',
                            max_length=200, )
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.name}: {self.price} р.'


class Levels(models.Model):
    quantity = models.IntegerField('Количество',
                                   choices=[(1, 1), (2, 2), (3, 3)],
                                   default=1)
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])
    def __str__(self):
        return f'{self.quantity}: {self.price} р.'


class Berries(models.Model):
    name = models.CharField('Название',
                            max_length=200, )
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.name}: {self.price} р.'


class Decoration(models.Model):
    name = models.CharField('Название',
                            max_length=200, )
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.name}: {self.price} р.'


class Cake(models.Model):
    name = models.CharField(
        'Название',
        blank=True,
        max_length=300)

    class Categories(models.TextChoices):
        TEA_PARTY = 'TEA_PARTY', 'На чаепитие'
        BIRTHDAY_PARTY = 'BIRTHDAY_PARTY', 'На день рождения'
        WEDDING = 'WEDDING', 'На свадьбу'
        CUSTOM = 'CUSTOM', 'На заказ'

    category = models.CharField(
        'Категория торта',
        choices=Categories.choices,
        default=Categories.CUSTOM,
        max_length=200)

    image = models.ImageField('Изображение торта',
                              null=True,
                              blank=True)

    levels = models.ForeignKey(Levels,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='cakes',
                               verbose_name='Количество уровней')
    form = models.ForeignKey(Form,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='cakes',
                             verbose_name='Форма')
    topping = models.ForeignKey(Topping,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='cakes',
                                verbose_name='Топпинг')
    berries = models.ForeignKey(Berries,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='cakes',
                                verbose_name='Ягоды')
    inscription = models.CharField('Надпись',
                                   max_length=300,
                                   blank=True)
    decoration = models.ForeignKey(Decoration,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='cakes',
                                   verbose_name='Декор')
    price = models.IntegerField('Цена',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.id}. {self.name} {self.category}'


class Client(models.Model):
    name = models.CharField('Имя клиента',
                            max_length=200,
                            db_index=True)
    email = models.EmailField('Почта клиента')
    phone_number = PhoneNumberField('Телефонный номер клиента',
                                    region='RU',
                                    max_length=20,
                                    unique=True)

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class Order(models.Model):
    cake = models.ManyToManyField(Cake,
                                  related_name='orders',
                                  verbose_name='Торт')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Клиент')
    comment = models.TextField('Комментарий к заказу',
                               blank=True)
    address = models.CharField('Адрес доставки',
                               max_length=350)
    delivery_date_time = models.DateTimeField('День и время доставки',
                                              db_index=True)

    class Statuses(models.TextChoices):
        TBA = 'TBA', 'На уточнении'
        ASSEMBLING = 'ASSEMBLING', 'Собирается'
        DELIVERING = 'DELIVERING', 'Доставляется'
        DONE = 'DONE', 'Выполнен'

    status = models.CharField('Статус заказа',
                              choices=Statuses.choices,
                              default=Statuses.TBA,
                              max_length=100)
    courier_comment = models.TextField('Комментарий для курьера',
                                       blank=True)
    cost = models.IntegerField('Стоимость',
                                default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(1000000),
                                ])

    def __str__(self):
        return f'{self.id} {self.client.name} {self.delivery_date_time}'

