import wikipedia

# for debugging purposes
def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)

# @deprecated
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

def has_wiki_page(query):
    search_lst = wikipedia.search(query)
    page = wikipedia.page(search_lst[0])
    if not page:
        return False
    return True
    
def get_wiki_page(query, category):
    # get first result of search query
    page = wikipedia.page(wikipedia.search(query)[0])
    # parse and save page plot to database(if not already existing page)
    content = str(page.content)
    plot_start = content.split("== Plot ==")[1]
    plot = plot_start.split("== ")[0]
    return plot