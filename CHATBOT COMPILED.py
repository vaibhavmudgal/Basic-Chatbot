
# coding: utf-8

# In[ ]:


base_link = 'https://www.poetryfoundation.org/search?query='     #base_link + 'genre of poem'
meaning_base_link = 'https://www.momjunction.com/baby-names/'
from bs4 import BeautifulSoup as bs
import urllib.request
import requests
import random
from textblob import TextBlob
from itertools import cycle
import pandas as pd
from IPython.core.display import HTML


# In[ ]:


name = input('Hi, what is your name? [answer in one word]   Your reply -> ')

name_meaning_link = meaning_base_link + name +'/'

list_no_tags = []

text = requests.get(name_meaning_link).text         #requesting for page
soup = bs(text,'lxml')              
s = soup.find_all(['label', 'span'])                #finding all the codes with the given tags

for i in range(len(s)):
    try:
        s1 = str(s[i]).split('>')
        s2 = s1[1].split('<')
        list_no_tags.append(s2[0])
    except:
        pass
    
def meaning(list_no_tags):
    for i in range(len(list_no_tags)):
        if name in list_no_tags[i].lower():
                m = list_no_tags[i+2]
                return m    
first_name = ['What a name!!', 'Nice name.', 'I like your name. ', 'I wish i had the same name.']
try:
    print(random.choice(first_name) + ' Do you know the meaning of your name is ' + meaning(list_no_tags))  
except:
    print(random.choice(first_name))




feeling = input('Okay ' + name.upper() + '!' + 'How are you feeling today?' +'  '+ name.upper() +  ' -> ')

blob = TextBlob(feeling)
sentence = blob.sentences[0]
for word, pos in sentence.tags:      # word --> word itself, pos --> part of speech
    if pos == 'JJ' or pos== 'NN':
        feels = word

poem_link = base_link +  feels   + '&refinement=poems'


print('The poem based on ' + feels +  ' feeling is: ')
print('\n')




all_links = []         #contains the link of the poems based on how user is feeling
req_links = []

text = requests.get(poem_link).text
soup = bs(text, 'lxml')
s = soup.find_all('a')
for i in s:
    if (feels and '/poems/') in str(i) and 'browse#' not in str(i) and '/guides' not in str(i) and '/poem-of-the-day' not in str(i):
        req_links.append(i)
for link in req_links:
     all_links.append(link.get('href'))
     
    
    
text = requests.get(all_links[random.choice(range(len(all_links)))]).text
soup = bs(text, 'lxml')
for line in soup.find_all(style="text-indent: -1em; padding-left: 1em;"):         #extracting text with given style tag
    print(line.text)        
    
    

    
its = []     #its --> item to search


print(name.upper() + ', do you want to shop online?')
response_1 = input()
if 'yes' in response_1.lower():
    print('Okay then, what would you want me to search for you?')
    resp_search = input()
    blob = TextBlob(resp_search)
    sentence = blob.sentences[0]
    for word, pos in sentence.tags:      # word --> word itself, pos --> part of speech
        if pos == 'NN' or pos == 'NNS':
            its.append(word)
s = '+'
x = s.join(its)


from lxml.html import fromstring
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:61]:
        #if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies



from itertools import cycle

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

link = '_______'               #enter the web address to scrap the website for products


proxies = get_proxies()
proxy_pool = cycle(proxies)
for i in range(1,11):
    #Get a proxy from the pool
    #proxy = next(proxy_pool)
    proxy = proxies[random.choice(range(61))]                          
    print(proxy)
    print("Request #%d"%i)
    try:
        text = requests.get(link, headers=headers, proxies={"http": proxy, "https": proxy}).text
        if "Sorry, we just need to make sure you're not a robot" in text:
            print('Blocked Due To Automated Access')
            pass
        else:
            break
    except:
        print('Skipping, Connection error')

soup = bs(text, 'lxml')
s = soup.find_all('a')




item_img_links = []
name_of_item = []



book_links = []
for i in s:
    if '/ref=sr_' in str(i) and '?keywords=' in str(i):
        book_links.append(i)
    else:
        pass

for i in range(len(book_links)):
    try:
        item_img_links.append(book_links[i].find('img').get('src'))
        name_of_item.append(book_links[i].find('img').get('alt'))
    except:
        pass

fin_list = []
for i in range(len(item_img_links)):
    fin_list.append(list([name_of_item[i], item_img_links[i]]))




import pandas as pd
from IPython.core.display import HTML




df = pd.DataFrame(fin_list, columns = ['NAME', 'image'])

#df['image'] = item_img_links

def path_to_image_html(path):
    return '<a href="'+ path +'"><img src="'+ path + '" width="60" >'
#df
pd.set_option('display.max_colwidth', -1)
HTML(df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))


# In[23]:


x = range(1,10)
random.sample(range(1,10),4)

