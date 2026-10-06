import re
from html.parser import HTMLParser

class StandardsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.in_overlay = False
        self.current_tag = []
        self.output = "# Standards Content Review\n\n"
        
        self.cards = []
        self.current_card = {}
        
        self.overlays = []
        self.current_overlay = {}
        self.current_detail = {}
        self.in_table = False

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r') as f:
    html = f.read()

# I will use a simpler approach with BeautifulSoup since it's easier, or regex if bs4 fails.
