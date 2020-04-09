import csv
import os
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# target = 'https://www.gouvernement.lu/coronavirus'
# target = 'https://gouvernement.lu/fr/dossiers.gouv_msan+fr+dossiers+2020+corona-virus.html'
target = 'https://www.worldometers.info/coronavirus/#countries'
headers = {'content-type': 'application/json,text/html,application/xhtml+xml,application/xml', 'Accept-Charset': 'UTF-8'}

# headers = {
#     'Host': 'www.gouvernement.lu',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en-GB,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1'
# }


def csv_read_lastline(file):
    csvFile = open(file, "r")
    reader = csv.reader(csvFile)
    lastline = None
    for item in reader:
        lastline = item
    csvFile.close()
    return lastline


def csv_write_lastline(file, d1, d2):
    csvFile = open(file, "a")
    writer = csv.writer(csvFile)
    writer.writerow([d1, d2])
    csvFile.close()


def csv_change_lastline(file, d1, d2):
    tmp = str(file) + '_tmp'
    with open(file) as inf, open(tmp, 'w') as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        for line in reader:
            if line[0] == d1:
                writer.writerow([d1, d2])
            else:
                writer.writerow(line)
    os.remove(file)
    os.rename(tmp, file)


def change_file(file, d):
    tmp = str(file) + '_tmp'
    with open(file) as inf, open(tmp, 'w') as outf:
        outf.write(inf.readline())
        new = str(d) + '</font>'
        outf.write(new)
    os.remove(file)
    os.rename(tmp, file)


if __name__ == '__main__':
    pattern1 = re.compile(r'>(((\d*)[,])*(\d+))</td>', re.I)
    pattern2 = re.compile(r'Luxembourg')
    pattern3 = re.compile(r'China')
    pattern4 = re.compile(r'Switzerland')
    pattern5 = re.compile(r'[A-Za-z]+ [0-9]{2}, [0-9]{4}')

    while(True):
        # Access page
        response = requests.get(target, auth=('user', 'pass'))
        soup = BeautifulSoup(response.text, "html.parser")
        datetimeStr = re.search(pattern5, str(soup)).group()
        datetimeObject = datetime.strptime(datetimeStr, '%B %d, %Y')
        current_date = str(datetimeObject.strftime('%Y-%m-%d').split('-')[0]) + str(datetimeObject.strftime('%Y-%m-%d').split('-')[1]) + str(datetimeObject.strftime('%Y-%m-%d').split('-')[2])

        myTable = "\"" + str(soup.find("table", {"id": "main_table_countries_today"})) + "\""
        soup = BeautifulSoup(myTable, "html.parser")

        luxembourgText = soup.find_all(text=re.compile('Luxembourg'))
        luxembourgTable = luxembourgText[0].parent
        luxembourgTable = luxembourgTable.parent.parent
        luxembourgArray = str(luxembourgTable).split('font-weight')
        luxembourgTotal = re.findall(r'\d+', luxembourgArray[2].replace(",", ""))[0]
        luxembourgDeath = re.findall(r'\d+', luxembourgArray[4].replace(",", ""))[0]
        luxembourgRecover = re.findall(r'\d+', luxembourgArray[6].replace(",", ""))[0]

        chinaText = soup.find_all(text=re.compile('China'))
        chinaTable = chinaText[0].parent
        chinaTable = chinaTable.parent.parent
        chinaArray = str(chinaTable).split('font-weight')
        chinaTotal = re.findall(r'\d+', chinaArray[2].replace(",", ""))
        chinaDeath = re.findall(r'\d+', chinaArray[4].replace(",", ""))
        chinaRecover = re.findall(r'\d+', chinaArray[6].replace(",", ""))

        switzerlandText = soup.find_all(text=re.compile('Switzerland'))
        switzerlandTable = switzerlandText[0].parent
        switzerlandTable = switzerlandTable.parent.parent
        switzerlandArray = str(switzerlandTable).split('font-weight')
        switzerlandTotal = re.findall(r'\d+', switzerlandArray[2].replace(",", ""))
        switzerlandDeath = re.findall(r'\d+', switzerlandArray[4].replace(",", ""))
        switzerlandRecover = re.findall(r'\d+', switzerlandArray[6].replace(",", ""))

        if_changed = False
        if_date_remain = True

        # Read confirmed csv
        lastline = csv_read_lastline("case_confirmed_luxembourg.csv")
        if lastline[0] != current_date:
            print('Add new confirmed data ' + luxembourgTotal +
                  ' @' + str(datetime.now()))
            if_changed = True
            if_date_remain = False
            last_confirmed = lastline[1]
            change_file('subpage_confirmed_luxembourg.html', luxembourgTotal)
            csv_write_lastline("case_confirmed_luxembourg.csv", current_date, luxembourgTotal)
        elif lastline[1] != luxembourgTotal:
            print('Modified confirmed data from ' +
                  lastline[1] + ' to ' + luxembourgTotal + ' @' + str(datetime.now()))
            if_changed = True
            last_confirmed = lastline[1]
            change_file('subpage_confirmed_luxembourg.html', luxembourgTotal)
            csv_change_lastline("case_confirmed_luxembourg.csv", current_date, luxembourgTotal)

        # Read died csv
        lastline = csv_read_lastline("case_died_luxembourg.csv")
        if lastline[0] != current_date:
            print('Add new died data ' + str(luxembourgDeath) +
                  ' @' + str(datetime.now()))
            if_changed = True
            if_date_remain = False
            change_file('subpage_died_luxembourg.html', luxembourgDeath)
            csv_write_lastline("case_died_luxembourg.csv", current_date, luxembourgDeath)
        elif lastline[1] != luxembourgDeath:
            print('Modified died data from ' +
                  lastline[1] + ' to ' + luxembourgDeath + ' @' + str(datetime.now()))
            if_changed = True
            change_file('subpage_died_luxembourg.html', luxembourgDeath)
            csv_change_lastline("case_died_luxembourg.csv", current_date, luxembourgDeath)

        # Read recovered csv
        lastline = csv_read_lastline("case_recovered_luxembourg.csv")
        if lastline[0] != current_date:
            print('Add new recovered data ' + luxembourgRecover +
                  ' @' + str(datetime.now()))
            if_changed = True
            if_date_remain = False
            change_file('subpage_recovered_luxembourg.html', luxembourgRecover)
            csv_write_lastline("case_recovered_luxembourg.csv", current_date, luxembourgRecover)
        elif lastline[1] != luxembourgRecover:
            print('Modified recovered data from ' +
                  lastline[1] + ' to ' + luxembourgRecover + ' @' + str(datetime.now()))
            if_changed = True
            change_file('subpage_recovered_luxembourg.html', luxembourgRecover)
            csv_change_lastline("case_recovered_luxembourg.csv", current_date, luxembourgRecover)

        if if_changed:
            if not if_date_remain:
                change_file('subpage_date_luxembourg.html', datetimeStr)
                if_date_remain = True

            # Change Table
            new_table_line = '| ' + str(datetimeObject.day) + '.' + str(datetimeObject.month)
            diff_c = int(luxembourgTotal) - int(last_confirmed)
            new_table_line += ' | (+' + str(diff_c) + ')'
            new_table_line += ' | ' + luxembourgTotal
            new_table_line += ' | ' + luxembourgRecover
            new_table_line += ' | ' + luxembourgDeath + ' | |\n'

            with open('table.md', 'a') as table_file:
                table_file.write(new_table_line)

            print('===\nRebuild table')
            # os.system('git pull')
            # os.system('markdown table.md > table.html')
            # os.system('git add .')
            # commit_msg = 'git commit -m "Table @' + str(datetime.datetime.now()) + '"'
            # os.system(commit_msg)
            # os.system('git push')

            print('===\nRebuild Plot')
            # os.system('git pull')
            exec(open('make_plot.py').read())
            print('Push to github')
            # os.system('git add .')
            # commit_msg = 'git commit -m "Plot @' + str(datetime.datetime.now()) + '"'
            # os.system(commit_msg)
            # os.system('git push')
            if_changed = False

        print('Checked at ' + str(datetime.now()))
        time.sleep(60)
