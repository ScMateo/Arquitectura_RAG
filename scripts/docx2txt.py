import re, html, sys, zipfile

def docx_to_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read('word/document.xml').decode('utf-8', 'ignore')
    x = x.replace('</w:p>', '\n')
    x = x.replace('</w:tr>', '\n')
    x = x.replace('</w:tc>', ' | ')
    x = re.sub(r'<[^>]+>', '', x)
    return html.unescape(x)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print('=' * 20, p, '=' * 20)
        try:
            print(docx_to_text(p))
        except Exception as e:
            print('ERROR:', e)
