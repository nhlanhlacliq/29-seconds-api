import wikipedia

class WikiPage():
    has_page = False
    page = None
    query = None

    def __init__(self, query):
        result = wikipedia.search(query)[0]
        page = wikipedia.page(result, auto_suggest=False)

        if page:
            self.has_page = True
            self.page = page
            self.query = query

    # for debugging purposes
    # @deprecated
    def print_sections(self, sections, level=0):
        for s in sections:
            print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
            print_sections(s.sections, level + 1)

    # @deprecated
    def get_summary(self, sections, level=0):
        data = ''
        # for s in sections:
        #     print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        #     continue
        data = str(sections[0])
        data = data.replace("Plot","")
        data = data.replace("Subsections","")
        data = data.replace("Section","")

        return data

    def has_page(self):
        return self.has_page

    def get_data(self):
        try:
            # parse and save page plot to database(if not already existing page)
            title = str(self.page.title)
            content = str(self.page.content)
            # print(content)
            plot = content.split("==")[2]
            if len(plot) < 10:
                plot = content.split("==")[4]
            return title, plot
        except IndexError:
            return f"'{query}' has no plot/synopsis."