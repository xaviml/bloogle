from readability import Document
from bs4 import BeautifulSoup

def HTMLparser(page, blog):
    #doc = Document(body)
    #doc.short_title() -> short title
    #doc.summary() -> body (clean the html tags)
    # Maybe extract more attributes apart from title and content
    title = 'title'
    content = 'content'

    soup = BeautifulSoup(page)
    if blog == 'medium':
        article = soup.find('div',{'class':'section-content'})
    elif blog == 'gizmodo':
        article = soup.find('div',{'class':'post-content'})
    elif blog == 'steemit':
        article = soup.find('div',{'class':'PostFull__body'})
    elif blog == 'techcrunch':
        article = soup.find('div',{'class':'article-content'})
    elif blog == 'theverge':
        article = soup.find('div',{'class':'c-entry-content'})
    elif blog == 'wired':
        article = soup.find('article')

    title = soup.title.string

    if article is not None:
        content = (article.get_text(" "))
        print(content)
    return {
        'title': title,
        'content': content
    }
