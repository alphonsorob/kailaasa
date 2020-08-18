import requests, csv, bs4
from tqdm import tqdm

fromY = int(input('Enter Start Year (included): '))
toY = int(input('Enter End Year (included): '))

day_urls = []

print('Parsing All Data..')
for year in range(fromY, toY+1):
    year_url = 'https://nithyanandapedia.org/index.php?title=Category:'+str(year)
    web_html = requests.get(year_url)
    bso = bs4.BeautifulSoup(web_html.text, 'html.parser')

    days = bso.select('.mw-content-ltr ul li a')

    for day in days:
        day_urls.append('http://nithyanandapedia.org'+str(day.get('href')))

    if (bso.select('#mw-pages a') and bso.select('#mw-pages a')[0].text == 'next page'):
        #print('Passed If statement')
        year_url = 'http://nithyanandapedia.org'+bso.select('#mw-pages a')[0].get('href')
        web_html = requests.get(year_url)
        bso = bs4.BeautifulSoup(web_html.text, 'html.parser')

        days = bso.select('.mw-content-ltr ul li a')

        for day in days:
            day_urls.append('http://nithyanandapedia.org'+str(day.get('href')))

    if (bso.select('#mw-pages a') and bso.select('#mw-pages a')[0].text == 'next page'):
        #print('Passed 2nd If statement')
        year_url = 'http://nithyanandapedia.org'+bso.select('#mw-pages a')[0].get('href')
        web_html = requests.get(year_url)
        bso = bs4.BeautifulSoup(web_html.text, 'html.parser')

        days = bso.select('.mw-content-ltr ul li a')

        for day in days:
            day_urls.append('http://nithyanandapedia.org'+str(day.get('href')))


print('Found '+str(len(day_urls))+' pages..')
#print(day_urls[0])
#Collecting all youtube links

#print('Fetching all links..')


#Only for counting
'''
i = 0
for url in tqdm(day_urls, desc='Fetching all photos..'):
    web_html = requests.get(url)
    bso = bs4.BeautifulSoup(web_html.text, 'html.parser')
    if bso.select('.mw-parser-output .image') or bso.select('.mw-parser-output img'):
        sources = bso.select('.mw-parser-output .image') if bso.select('.mw-parser-output .image') else bso.select('.mw-parser-output img')
        for source in sources:
            i+=1
    
print(str(i)+' photos found.')
'''

#For fetching photo links
plinks = []
i = 0
for url in tqdm(day_urls, desc='Fetching all photos..'):
    web_html = requests.get(url)
    bso = bs4.BeautifulSoup(web_html.text, 'html.parser')
    if bso.select('.mw-parser-output .image') or bso.select('.mw-parser-output img'):
        sources = bso.select('.mw-parser-output .image') if bso.select('.mw-parser-output .image') else bso.select('.mw-parser-output img')
        dateStamp = bso.select('#firstHeading')[0].text
        for source in sources:
            i+=1
            pStamp = source.get('href') if bso.select('.image') else source.get('src')
            plinks.append([dateStamp, pStamp])


csv_file_name = 'photoData_'+str(fromY)+'_to_'+str(toY)+'.csv'
with open(csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Photo Link'])
    writer.writerows(plinks)

print(str(i)+' links exported to '+csv_file_name+'.')
