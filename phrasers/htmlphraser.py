import os

from bs4 import BeautifulSoup

from . import phraser

""".html format:
<html>
    <head>...</head>
    <body>
        <div class="container">
            ...
            <div id='start-with-i' class='row'>
                <div class='col-3 col-md-2'>
                    <div class='py-1 mt-1 text-center rounded border'>
                        <mark class="monofont">inum</mark>
                        <br>
                        <span>№</span>
                    </div>
                </div>
            </div>
            ...
        </div>
    </body>
</html>
"""


class HtmlPhraser(phraser.Phraser):
    ext = 'html'
    name = 'HTML'

    def from_file(self, filepath: str):
        # TODO
        """ Read file into objects."""
        if not filepath:
            raise Exception("No filepath provided")
        pass

    def to_file(self, filepath: str):
        if not filepath:
            raise Exception("No filepath provided")
        if os.path.exists(filepath):
            raise Exception("File '{}' already exists!".format(filepath))
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(self.to_html())

    def from_html(self, html_str: str):
        soup = BeautifulSoup(html_str, 'html.parser')
        for dct in soup.find_all('dict'):
            phrase = dct.find_all('string')[0].string
            shortcut = dct.find_all('string')[1].string
            self.phrases.append({'phrase': phrase, 'shortcut': shortcut})

    def to_html(self):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        soup = BeautifulSoup(open(os.path.join(dirpath, 'htmlphraser_tpl.html')), 'html.parser')
        phrases_div = soup.html.body.find(id='phrases')
        for itm in self.phrases:
            row_attrs = {
                'class': 'row',
                'id': 'start-with-{}'.format(itm['shortcut'][0])
            }
            row = soup.find(attrs=row_attrs)
            if not row:
                row = soup.new_tag('div', attrs=row_attrs)
                header = soup.new_tag('kbd', attrs={'class': 'col-12 text-center'})
                header.string = itm['shortcut'][0]
                row.append(header)
                phrases_div.append(row)
            col = soup.new_tag('div')
            col['class'] = 'col-3 col-md-2'
            phrs_item = soup.new_tag('div', attrs={'class': 'py-1 mt-1 text-center rounded border'})
            phrs_shortcut = soup.new_tag('mark', attrs={'class': 'monofont'})
            phrs_shortcut.string = itm['shortcut']
            phrs_br = soup.new_tag('br')
            phrs_phrase = soup.new_tag('span', attrs={'class': 'lead'})
            phrs_phrase.string = itm['phrase']
            phrs_item.append(phrs_shortcut)
            phrs_item.append(phrs_br)
            phrs_item.append(phrs_phrase)
            col.append(phrs_item)
            row.append(col)
        return str(soup)
