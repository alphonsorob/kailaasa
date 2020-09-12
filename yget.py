'''
This program downloads the inputed youtube videos into the current working directory along with info file

#Setting up conda environment
conda create --name yget
conda activate yget
conda install pip
pip install pytube3

#Running file inside conda environment
python yget.py ,link1, link2, link3,...

#Deactivating conda environment
conda deactivate
'''

from pytube import YouTube
from pytube.cli import on_progress
import sys, os, csv


if len(sys.argv) < 2:
	print('Usage: Please enter the video url after yget command.')
	sys.exit(1)

elif len(sys.argv) >= 2:
	inputs = len(sys.argv)-1
	import re
	queries = [str(sys.argv[i]) for i in range(1, inputs+1)]

	results = []
	for query in queries:
		if re.search(r'^(http)', query):
			url = query
			print('Video '+str(queries.index(query)+1))
			print('Accessing Youtube URL...')
		else:
			print('Searching Youtube...')
			from youtube_search import YoutubeSearch
			import json
			results = YoutubeSearch(query, max_results=10).to_json()
			results = json.loads(results)
			search_title = results['videos'][0]['title']
			print('Preparing to download', '-', search_title)
			while(1):
				key = input('\nProceed? (y/n): ')
				if key == 'n' or key == 'no':
					sys.exit(1)
				elif key == 'y' or key == 'yes':
					break
			url = 'https://www.youtube.com'+results['vidoeos'][0]['link']
			print('Accessing Youtube URL...')
		video = YouTube(url, on_progress_callback=on_progress)
		title = video.title
		description = video.description
		stream = video.streams.get_highest_resolution()
		file_size = round(stream.filesize/1000000, 2) 
		print('Downloading video... ['+str(file_size)+' MB]')
	
		# change file paths according to your system
		stream.download(filename=title)
		file_path = os.getcwd()+title+'.mp4'
		
		results.append([title, file_path, description])

		print('\n')

	csv_file_name = 'yt_info.csv'
	with open(csv_file_name, 'w', newline='') as file:
	    writer = csv.writer(file)
	    writer.writerow(['Video Title', 'Video Location', 'Video Description'])
	    writer.writerows(results)

	print('Results exported to '+csv_file_name+'.')
	print('Done.')

else:
	print('Invalid input. Check commands.')
