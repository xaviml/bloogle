from readability import Document
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime
from indexer.post import Post
import json

def HTMLparser(page, blog, url):
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
            datePublished = parse(datestring)
        if 'dateModified' in application_json_ld:
            datestring = application_json_ld['dateModified']
            dateModified = parse(datestring)
    
    if blog == 'steemit':
        author = soup.find('a',{'class':'ptc'}).get_text().split(" ")[0]
        datestring = soup.find('span',{'class':'updated'})['title'].split()[0]
        datePublished = parse(datestring)

    if len(content) < 500:
        return None
        
    return Post(
        meta={'id':url},
        title= title,
        content= content,
        author= author,
        datePublished= datePublished,
        dateModified= dateModified,
        url=url
    )