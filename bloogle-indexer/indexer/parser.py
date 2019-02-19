from readability import Document

def HTMLparser(body):
    doc = Document(body)
    #doc.short_title() -> short title
    #doc.summary() -> body (clean the html tags)
    # Maybe extract more attributes apart from title and content
    title = 'title'
    content = 'content'
    return {
        'title': title,
        'content': content
    }