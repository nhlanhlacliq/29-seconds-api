import wikipedia
from model import update_db

# for debugging purposes
def print_sections(sections, level=0):
    data = ''
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)
    return data

def get_summary(sections, level=0):
    data = ''
    # for s in sections:
    #     print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
    #     continue
    data = str(sections[0])
    data = data.replace("Plot","")
    data = data.replace("Subsections","")
    data = data.replace("Section","")

    return data

def has_wiki_page(query, category):
    # wiki = Wikipedia('en')
    search_lst = wikipedia.search(query)

    page_py = wikipedia.page(search_lst[0])
    # Return false if page does not exist
    if not page_py:
        return False
    # else save page to database(if not already existing page)
    result = get_summary(page_py.sections)
    # pass result onto model to check and add to database
    return update_db(query, category, result)