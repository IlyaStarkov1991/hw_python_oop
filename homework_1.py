import datetime as dt


class Record:
    def __init__(self, amount, date=dt.datetime.now(), comment=''):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date != dt.datetime.now():
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append((record.amount, record.date, record.comment))

    def get_today_stats(self):
        summ_day = 0
        current_date = dt.datetime.now()
        for rec in self.records:
            if rec[1].date() == current_date.date():
                summ_day += rec[0]
        return summ_day

    def get_week_stats(self):
        summ_week = 0
        current_date = dt.datetime.now()
        for rec in self.records:
            difference_date = current_date.date() - rec[1].date()
            if difference_date.days < 7:
                summ_week += rec[0]
        return summ_week


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories = self.get_today_stats()
        if calories < self.limit:
            remaining_calories = self.limit - calories
            print((f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью '
                   f'не более {remaining_calories: .2f} кКал'))
        else:
            print('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 97
    EURO_RATE = 105

    def get_today_cash_remained(self, currency='rub'):
        money_spendings = self.get_today_stats()
        money_limit = self.limit
        rate = 1
        if currency == 'usd':
            rate = self.USD_RATE
        elif currency == 'eur':
            rate = self.EURO_RATE

        if money_spendings < money_limit:
            balance = (money_limit - money_spendings) / rate
            print(f'На сегодня осталось {balance:.1f} {currency}')
        elif money_spendings == money_limit:
            print('Денег нет, держись')
        else:
            balance = (money_spendings - money_limit) / rate
            print(f'Денег нет, держись: твой долг - {balance:.1f} {currency}')


#  ТЕСТЫ КОДА

# date = dt.datetime.now() - dt.datetime.strptime('1.09.2023', '%d.%m.%Y')
# print(type(date.days))

# r1 = Record(amount=300, comment='Серёге за обед')
# print(r1.date)

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))

# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))

# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='07.09.2023'))

print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_week_stats())
# должно напечататься
# # На сегодня осталось 555 руб