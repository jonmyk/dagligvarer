from classes import Year, Month, Week__, Day, Transaction
from datetime import datetime
from isoweek import Week
import pandas as pd 

grocery_stores = "EUROSPAR|REMA|KIWI|EXTRA|OBS|JOKER|COOP|MATKROKEN|BP|SPAR"

class Parser:
    def __init__(self,filename):
        self.filename = filename      
        self.years = []
        self.months = []
        self.weeks = []
        self.dates = []
        self.transactions = []
        self.yearly_spending = 0
        self.monthly_spending = 0
        self.weekly_spending = 0
        self.daily_spending = 0

        self.next_date = None
        self.next_week = None
        self.next_month = None
        self.next_year = None
        self.current_date = None
        self.current_week = None
        self.current_month = None
        self.current_year = None

    def pandas_data(self):
        """Creates a pandas dataframe of the csv file"""
        df = pd.read_csv(self.filename, sep=',', encoding='utf-8-sig')
        purchases = df.loc[df["Type"] == "PURCHASE"]
        grocery = purchases.loc[df["Beskrivelse"].str.contains(grocery_stores, regex=True)]

        daily_fee = 0
        weekly_fee = 0
        monthly_fee = 0
        yearly_fee = 0
    
        for count, row in enumerate(grocery.itertuples()):
            if count != len(grocery) - 1:
                self.next_date = grocery[['Dato']].iloc[count+1]["Dato"]
                self.next_week = self.week_number(self.next_date)
                self.next_month = str(grocery[['Dato']].iloc[count+1]["Dato"])[3:5]
                self.next_year = str(grocery[['Dato']].iloc[count+1]["Dato"])[6:10]
            
            self.current_date = row.Dato
            self.current_week = self.week_number(row.Dato)
            self.current_month = row.Dato[3:5]
            self.current_year = row.Dato[6:10]
            fee = str(row.Beløp)[1:]
            description = row.Beskrivelse
            self.transactions.append(Transaction(self.current_date, description, fee))
            
            daily_fee += float(fee)
            weekly_fee += float(fee)
            monthly_fee += float(fee)
            yearly_fee += float(fee)

            if count == len(grocery) -1:
                self.dates.append(Day(self.current_date, self.transactions, daily_fee))
                self.weeks.append(Week__(self.current_year, self.current_week, weekly_fee))
                self.months.append(Month(self.current_year, self.current_month, monthly_fee))
                self.years.append(Year(self.current_year, yearly_fee))
                continue

            if self.current_date != self.next_date:
                self.dates.append(Day(self.current_date, self.transactions, daily_fee))
                self.transactions = []
                daily_fee = 0

            if self.current_week != self.next_week:
                self.weeks.append(Week__(self.current_year, self.current_week, weekly_fee))
                weekly_fee = 0

            if self.current_month != self.next_month:
                self.months.append(Month(self.current_year, self.current_month, monthly_fee))
                monthly_fee = 0

            if self.current_year != self.next_year:
                self.years.append(Year(self.current_year, yearly_fee))
                yearly_fee = 0
                
    def week_number(self, date):
        return int(str(Week.withdate(datetime.strptime(date,"%d.%m.%Y")))[5:7])

    def parse_data(self):
        """Parses the data and prints it to the console"""
        for y in self.years:
            print(f'{y.__str__()}')
            for m in self.months:
                if y.year == m.year:
                    print(f'{m.__str__()}')
                    for w in self.weeks:
                        if m.month == w.month[0]:
                            print(f'{w.__str__()}')
                            for d in self.dates:
                                if w.week == d.week:
                                    print(f'{d.__str__()}')
                            print("\n")    

    def calculate_average(self, string, list):
        """Calculates the average spending for each year, month, week and day"""
        total = 0
        for i in list:
            total += float(i.spending)
        average_spending = total / len(list)
        print(f'Average {string} spending: {average_spending:.2f} NOK')

    def present_averages(self):
        """Prints the average spending for each year, month, week and day"""
        print("------------------------------------------------------------------------------------------------------------------------------------")
        self.calculate_average("yearly", self.years)
        self.calculate_average("monthly", self.months)
        self.calculate_average("weekly", self.weeks)
        self.calculate_average("daily", self.dates)
        print("------------------------------------------------------------------------------------------------------------------------------------\n")


if __name__ == '__main__':
    parser = Parser('report-FPPqV-2021114.csv')
    parser.pandas_data()
    parser.parse_data()
    parser.present_averages()








