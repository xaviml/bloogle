from readability import Document
from bs4 import BeautifulSoup
from datetime import datetime
from .blog_item import BlogItem
import json

def HTMLparser(page, blog):
    title = None
    content = None
    author = None
    datePublished = None
    dateModified = None

    soup = BeautifulSoup(page, 'lxml')
    doc = Document(page)
    title = doc.short_title()
    content = BeautifulSoup(doc.summary(), 'lxml').get_text()
    try:
        application_json_ld = json.loads(soup.find('script',{'type':'application/ld+json'}).get_text())
    except:
        application_json_ld = None
    if application_json_ld is not None:
        if 'author' in application_json_ld:
            if isinstance(application_json_ld['author'], list):
                author = application_json_ld['author'][0]['name']
            else:
                author = application_json_ld['author']['name']
        if 'datePublished' in application_json_ld:
            datestring = application_json_ld['datePublished']
            datePublished = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ')
        if 'dateModified' in application_json_ld:
            datestring = application_json_ld['dateModified']
            dateModified = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ')
    
    if blog == 'steemit':
        author = soup.find('a',{'class':'ptc'}).get_text().split(" ")[0]
        datestring = soup.find('span',{'class':'updated'})['title'].split()[0]
        datePublished = datetime.strptime(datestring, '%m/%d/%Y')

    item = BlogItem()
    item.title = title
    item.content = content
    item.author = author
    item.datePublished = datePublished
    item.dateModified = dateModified
    return item