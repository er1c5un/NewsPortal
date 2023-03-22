from datetime import datetime

from django.db import models

director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]


class Staff(models.Model):
    full_name = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField(default=0)
    note_1 = models.TextField(null=True)

    def get_last_name(self):
        return self.full_name.split()[0]


class Product(models.Model):
    name = models.CharField(max_length=255, default='')
    price = models.FloatField(default=0.0)


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            duration = (self.time_out - self.time_in).total_seconds()
        else:
            duration = (self.time_out - datetime.now()).total_seconds()
        return duration // 60


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


if __name__ == "__main__":
    fri_stand = Product(name='Картофель фри (Станд)', price=93)
    fri_stand.save()
    fri_big = Product.objects.create(name='Картофель фри (Бол)', price=100)
