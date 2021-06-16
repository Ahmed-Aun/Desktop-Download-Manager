import pafy

url = input('Enter URL: ')
list = pafy.get_playlist(url)
print(list['title'])

'''
videos = list['items']
print(videos)

for vid in videos:
    p = vid['pafy']
'''



################################
'''
link = input('Enter the url: ')
v = pafy.new(link)
print(v.title)
print(v.duration)
print(v.rating)
print(v.author)
print(v.length)
print(v.thumb)
print(v.videoid)
print(v.viewcount)
st = v.allstreams
for s in st:
    print(s.mediatype, s.resolution, s.extension, s. quality, s.get_filesize())

'''