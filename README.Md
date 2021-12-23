# Dagligvarer
Scriptet analyserer kontoutskrift fra bank, og returnerer ut en oversikt over det ukentlige, månedlige og årlige forbruket i dagligvarer. 

Fungerer for kontoutskrift fra Sparebanken Sogn og Fjordane.

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
3. legg til kontoutskriften (csv-fil) i samme mappe som main.py og classes.py, og endre scriptet (linje 138). 
```py
parser = Parser('report.csv')
```
4. kjør koden i terminalen
  ```sh
  python3 main.py
  ```
