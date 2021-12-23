from isoweek import Week
from datetime import datetime


class Year:
    """A year object holds the year together with the total spending within that year.
    """
    def __init__(self, year, spending) -> None:
        self.year = int(year)
        self.spending = "%.02f" % spending
        self.months = 12
        self.total_weeks = self.week_number()
        self.dates = []
        self.dates_in_year()
    
    def week_number(self) -> int:
        """Returns the total number of weeks within a given calendar year."""
        return Week.last_week_of_year(int(self.year))[1]

    def dates_in_year(self) -> None:
        """Appends all the dates within the year of the object to a list."""
        weeks = self.week_number()
        for week in range(1,weeks+1):
            for day in range(0,7):
                date = Week(self.year,week).day(day).strftime("%d.%m.%Y")
                self.dates.append(date)
    
    def __str__(self):
        return f'{self.year} - {self.spending} NOK\n\n'

class Month(Year):
    """ A month object contains a year, a month and a spending.
    """
    def __init__(self, year,  month, spending) -> None:
        super(Year,self).__init__()
        self.year = int(year)
        self.month = int(month)
        self.spending =  "%.02f" % spending
        self.dates = []
        self.weeks = []
        self.dates_in_month()
        self.weeks_in_month()

    def dates_in_month(self) -> None:
        """Appends all the dates within the month of the object to a list"""
        weeks = self.week_number()
        for week in range(1,weeks+1):
            dates = Week(self.year,week).days()
            for date in dates:
                month = '%d' % int(str(date)[5:7])
                year = str(date)[:4]
                if month == self.month and year == self.year:
                    self.dates.append(date.strftime("%d.%m.%Y"))
                
    def weeks_in_month(self) -> None:
        """Appends all the weeks within the month of the object to a list"""
        for date in self.dates:
            date_tm = datetime.strptime(date,"%d.%m.%Y")
            current_week = date_tm.isocalendar()[1]
            if current_week not in self.weeks:
                self.weeks.append(current_week)

    def month_name(self) -> str:
        return datetime.strptime(str(self.month), "%m").strftime("%B")

    def __str__(self) -> str:
        month = self.month_name()
        return f"\t{month} - {self.spending} NOK\n\n"

class Week__:
    """ A week class object holds a week number. A week can have two months or years within it.
    """
    def __init__(self, year, week, spending) -> None:
        self.week = int(week)
        self.year = int(year)
        self.spending = "%.02f" % spending
        self.dates = []
        self.dates_in_week()
        self.month = self.months_in_week()

    def dates_in_week(self) -> None:
        dates = Week(self.year,self.week).days()
        for date in dates:
            self.dates.append(date.strftime("%d.%m.%Y"))

    def week_dates(self) -> str:
        """Returns a string representing the dates within the week"""
        monday = self.dates[0][0:2]
        sunday = self.dates[6][0:2]
        month_1 = self.dates[0][3:5]
        month_2 = self.dates[6][3:5]
        month_name_1 = datetime.strptime(month_1,"%m").strftime("%B").lower()[0:3]
        month_name_2 = datetime.strptime(month_2,"%m").strftime("%B").lower()[0:3]
        return f"({monday}.{month_name_1}-{sunday}.{month_name_2})"

    def months_in_week(self) -> list:
        """Returns a list of the months that resides within the given week"""
        months = []
        for date in self.dates:
            month = date[3:5]
            if month not in months:
                months.append(int(month))
        return months

    def __str__(self) -> str:
        dates = self.week_dates()
        return f"\t\tweek {self.week} {dates}: {self.spending} NOK\n"

class Day:
    """ A day object holds a single date. It has a year, month, week and spending.
    """

    def __init__(self, date, transactions, spending) -> None:
        self.date = date
        self.year = int(self.date[6:10])
        self.month = int(self.date[3:5])
        self.week = int(self.week_of_date())
        self.spending = "%.02f" % spending
        self.transactions = transactions
        self.week_day = self.day_of_week()

    def day_of_week(self) -> int:
        """Returns the weekday name of the object's date"""
        date = datetime.strptime(self.date,"%d.%m.%Y")
        return date.strftime("%A")

    def week_of_date(self) -> str:
        """Returns the week number of the object's date"""
        date_tm = datetime.strptime(self.date,"%d.%m.%Y")
        return '%d' % int(str(Week.withdate(datetime.date(date_tm)))[5:])

    def __str__(self) -> str:
        spaces = len(f'{self.week_day} ({self.date}): {self.spending} NOK     ')
        txt_space = "\n\t\t\t".ljust(spaces)
        transactions = txt_space.join(map(str, self.transactions))

        return f"\t\t\t{self.week_day} ({self.date}): {self.spending} NOK {transactions}\n\n"

class Transaction(Day):
    """ A transaction object holds a single date, a transaction description and a fee.
    """

    def __init__(self, date, transaction, amount) -> None:
        super(Day,self).__init__()
        self.date = date
        self.week_day = self.day_of_week()
        self.transaction = transaction
        self.amount = amount

    def __str__(self) -> str:
        return f"   (See: {self.transaction}, {self.amount} NOK)"
