from readability import Document
from bs4 import BeautifulSoup
from datetime import datetime

def HTMLparser(page, blog):
    #doc = Document(body)
    #doc.short_title() -> short title
    #doc.summary() -> body (clean the html tags)
    # Maybe extract more attributes apart from title and content
    title = ''
    content = ''
    author = ''
    date = None

    soup = BeautifulSoup(page)

    if blog == 'medium':
        article = soup.find('div',{'class':'section-content'})
        author = soup.find('meta', {'property':'author'})["content"]
        #datestring = soup.find('meta', {'property':'article:published_time'})["content"].split("T")[0]
        #date = datetime.strptime(datestring,'%Y-%m-%d')

    elif blog == 'gizmodo':
        article = soup.find('div',{'class':'post-content'})
        author = soup.find('meta', {'name':'author'})["content"]
        datestring = soup.find('time',{'class':'meta__time updated'})['datetime'].split("T")[0]
        date = datetime.strptime(datestring,'%Y-%m-%d')

    elif blog == 'steemit':
        article = soup.find('div',{'class':'PostFull__body'})
        author = soup.find('a',{'class':'ptc'}).get_text().split(" ")[0]
        datestring = soup.find('span',{'class':'updated'})['title'].split()[0]
        date = datetime.strptime(datestring, '%m/%d/%Y')

    elif blog == 'techcrunch':
        article = soup.find('div',{'class':'article-content'})
        #author = soup.find('meta', {'name':'sailthru.author'})["content"] #author tag in html but not scraped for some reason
        datestring = soup.find('meta', {'name':'sailthru.date'})["content"].split()[0]
        date = datetime.strptime(datestring,'%Y-%m-%d')

    elif blog == 'theverge':
        article = soup.find('div',{'class':'c-entry-content'})
        author = soup.find('meta', {'property':'author'})["content"]
        datestring = soup.find('meta', {'property':'article:published_time'})["content"].split("T")[0]
        date = datetime.strptime(datestring,'%Y-%m-%d')


    elif blog == 'wired':
        article = soup.find('article')
        author = soup.find('meta', {'name':'parsely-author'})["content"]
        datestring = soup.find('meta', {'name':'parsely-pub-date'})["content"].split("T")[0]
        date = datetime.strptime(datestring,'%Y-%m-%d')

    title = soup.title.string

    if article is not None:
        content = (article.get_text(" "))


    return {
        'title': title,
        'content': content,
        'author': author,
        'date': date
    }