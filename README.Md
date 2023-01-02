# Dagligvarer
Et script som gir deg en utskrift og oversikt over ditt ukentlige, månedlige og årlige forbruk i dagligvarer.

# Bruk

 1. klon repoet
```sh
git clone https://github.com/jonmyk/dagligvarer.git
```
 2. installer nødvendige bibliotek
```sh
pip3 install datetime
pip3 install isoweek
pip3 install pandas
```
3. legg til kontoutskriftsfilen i samme mappe som main.py og classes.py, og endre scriptet main.py (linje 122). 
```py
parser = Parser('report.csv')
```
4. kjør koden i terminalen
```sh
python3 main.py
```
