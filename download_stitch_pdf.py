import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger, PdfFileReader

def next_button_filter(tag): 
    return (len(tag.contents) == 1 and tag.contents[0].name == 'img' and tag.img.get('alt') == 'Next Page')


def get_article_title(soup):
    return soup.find('span', 'articletitle').string

if __name__=="__main__":
	prefix = 'http://quod.lib.umich.edu'
	nextlink = 'http://quod.lib.umich.edu/m/mqrarchive/act2080.0031.004/120?view=pdf&size=100'
	r = requests.get(nextlink)
	soup = BeautifulSoup(r.text)
	orig_title = get_article_title(soup)
	filename = orig_title.lower().replace(":", "").replace("/", "").replace(" ", "-")
	print "Article title: ", orig_title
	counter = 1
	numpages = 1

	while (nextlink):
	    r = requests.get(nextlink)
	    soup = BeautifulSoup(r.text)
	    title = get_article_title(soup)
	    if (title == orig_title):
		print "Adding page ", counter
		pdflink = prefix + soup.find_all('a')[-1].get('href')
		pdflinkresp = requests.get(pdflink)
		
		with open(str(counter) + '.pdf', 'wb') as fo: 
		        fo.write(pdflinkresp.content)
		
		pot_next_btns = soup.find_all(next_button_filter)
		nextlink = ""
		if len(pot_next_btns) == 1:
		    nextlink = pot_next_btns[0].get('href')
		counter += 1
	    else: 
		numpages = counter - 1
		print "Done"
		break


	merger = PdfFileMerger()
	counter = 1
	output = open(filename + ".pdf", "wb")

	while (counter <= numpages):
	    merger.append(PdfFileReader(file(str(counter)+'.pdf', 'rb')))
	    counter += 1

	merger.write(output)
	output.close()

