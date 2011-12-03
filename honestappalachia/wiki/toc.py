import re

from BeautifulSoup import BeautifulSoup as BS
from django.template.defaultfilters import slugify

def permalink_anchor(hs):
    '''Given a header string, build the permalink href attr'''
    return '#' + slugify(hs)

def genTOC(s):
    '''Generate TOC as OL from headers in s'''
    toc = []

    soup = BS(s)
    header_rgx = re.compile(r'[Hh]([1-6])')

    current_level = 0
    for h in soup.findAll(header_rgx):
        header_content = h.contents[0]
        header_level = h.name[1]
        if int(header_level) > current_level:
            toc.append("<ol>")
            current_level = int(header_level)
        elif int(header_level) < current_level:
            toc.append("</ol>")
            current_level = int(header_level)
        else: # header_level == current_level
            pass


        toc.append("<li>")
        toc.append('<a class="toclink" href="' + permalink_anchor(header_content)
                + '">' + header_content + '</a>')
        toc.append("</li>")

    # close last round of list tags
    for x in range(current_level):
        toc.append("</ol>")

    return ''.join(toc)

def header_permalinks(s):
    '''Add permalinks to headers'''
    soup = BS(s)
    header_rgx = re.compile(r'[Hh][1-6]')
    for h in soup.findAll(header_rgx):
        h.contents[-1].replaceWith(h.contents[-1] + " " +
        '<a class="permalink" href="' +
        permalink_anchor(h.contents[-1]) +
        '" title="Permalink to this section">&para;</a>')

    return soup.prettify()

def main():
    text = u"<h1>The Scoop</h1>\n<p>Honest Applachia is a <em>super kickass</em> organization that just got started in the Spring of 2011.</p>\n<h2>What's next</h2>\n<p>Some more really cool stuff. Ooh look a table of contents!</p>"

    # TOC
    #tocloc = r'\[TOC\]'
    #if re.search(tocloc, s): # toc requested?
    #    toc = genTOC(s)
    #    re.sub(tocloc, toc, s)

    print genTOC(text)
    print header_permalinks(text)

if __name__ == "__main__": main()
