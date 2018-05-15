from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import time
import json

def getData(url):
    # header = {'user-agent' : 'GoogleChrome (Windows 10); Yuly Haruka'}
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')

    item = {}

    # Get the Product's Brand
    br = bs.find('div', {'class' : 'prod-title'})
    brand = br.find('a')
    print ('Product brand :')
    print (brand.get_text())
    print()
    item['brand'] = brand.get_text()

    # Get the name of product
    f = br.find('h1')
    print ('Product name :')
    print (f.get_text())
    print ()
    item['name'] = f.get_text()

    # Get the product's categories
    item['categories'] = []
    print ('Category :')
    c = bs.find('div', {'class' : 'bc'})
    category = c.findAll('a', {'href' : '#'})
    for ctg in category :
        print (ctg.get_text())
        item['categories'].append(ctg.get_text())
    print()

    # Get the product's description
    desc = bs.find('meta', {'name' : 'description'})['content']
    print ('Product description :')
    print(desc)
    print ()
    item['description'] = desc

    # Get the product's price
    price = bs.find('div', {'class' : 'price'})
    p = price.get_text().strip()
    print ('Price : ')
    print (p)
    print
    item['price'] = p

    # Get the product's stock by its size
    ukuran = []
    ukuran = getStock(bs)
    print ('Stok Produk')
    item['stock'] = printStock(bs, ukuran)

    return item

# Get all of the link in one page
def getLink(link) :
    parse = BeautifulSoup(link, 'html.parser')

    url = []
    find = parse.findAll('li', {'id' : 'li-catalog'})
    for l in find :
        url.append(l.find('a')['href'])
    return url

# Iterate function to get the stock of the product
def getStock(bs) :
    ukuran = []
    comments = bs.findAll(string=lambda text:isinstance(text,Comment))
    for c in comments :
        if 'Stok Sisa' in c :
            ukuran.append(c[c.find('Stok Sisa ') + len('Stok Sisa ') : c.find('<',c.find('Stok Sisa ') + len('Stok Sisa '))])
    return ukuran

# Print all of the stock by its product's size
def printStock(bs, ukuran) :
    stock = []
    sz = bs.find('ul', {'id' : 'select-size'})
    size = sz.findAll('input',{'name' : 'size_category'})
    i = 0
    for s in size :
        stok = {}
        print ('Ukuran : ', s['value'])
        stok['size'] = s['value']
        print ('Stok Tersedia : ', ukuran[i])
        stok['stock'] = ukuran[i]
        stock.append(stok)
        i += 1
    return stock

########################################### MAIN PROGRAM ######################################################
url = []
link = urlopen('https://berrybenka.com/clothing/women')
url = getLink(link)
data = {}
data['items'] = []
for i in url :
    data['items'].append(getData(i))
    time.sleep(1)

with open('data.json', 'w') as file :
    file.write(json.dumps(data, indent = 2))
