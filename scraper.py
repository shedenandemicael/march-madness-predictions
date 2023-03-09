from bs4 import BeautifulSoup
import csv
import requests

URL = "https://www.numberfire.com/ncaab/teams/power-rankings/"
page = requests.get(URL)

# find tables of interest
soup = BeautifulSoup(page.content, "html.parser")
stats = soup.find_all("tbody", class_="projection-table__body")

# collect row data
name = stats[0].find_all("a", class_="small-hide")
logo = stats[0].find_all("img", class_="team-logo")
nerd = stats[1].find_all("td", class_="nerd")
consistency = stats[1].find_all("td", class_="consistency")
seed = stats[1].find_all("td", class_="tseed")

# write data to data.csv
filename = "data.csv"
fields = ["name", "mean", "var", "seed"]
with open(filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields) 
    for i in range(len(name)):
        row = [name[i].text.strip(), nerd[i].text.strip(), 
               consistency[i].text.strip(), seed[i].text.strip()]
        csvwriter.writerow(row)

# write links to logos to logos.csv
filename = "logos.csv"
fields = ["logos"]
with open(filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields) 
    for link in logo:
        row = [link["src"]]
        csvwriter.writerow(row)