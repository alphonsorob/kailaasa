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

#Only for counting
'''
i = 0
for url in day_urls:
    web_html = requests.get(url)
    bso = bs4.BeautifulSoup(web_html.text, 'html.parser')
    if bso.select('.embedvideo'):
        sources = bso.select('.embedvideo iframe')
        for source in sources:
            i+=1
    
print(str(i)+' links found.')
'''

# For fetching video links

vlinks = []
i = 0
for url in tqdm(day_urls, desc='Fetching all links..'):
    web_html = requests.get(url)
    bso = bs4.BeautifulSoup(web_html.text, 'html.parser')
    if bso.select('.embedvideo'):
        sources = bso.select('.embedvideo iframe')
        dateStamp = bso.select('#firstHeading')[0].text
        for source in sources:
            i+=1
            vStamp = 'http://www.youtube.com/watch/'+(source.get('src').partition('/embed/')[-1])[:-1]
            vlinks.append([dateStamp, vStamp])
        
csv_file_name = 'linkData_'+str(fromY)+'_to_'+str(toY)+'.csv'
with open(csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Video Link'])
    writer.writerows(vlinks)

print(str(i)+' links exported to '+csv_file_name+'.')
