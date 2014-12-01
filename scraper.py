# scraper for scraping the chinese dictionary off of 
# http://www.mdbg.net/chindict/chindict.php?page=radicals
# and stores it into a JSON object

import re, json, io
from pattern.web import URL, DOM, plaintext, strip_between
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT

chindict = {}
radicals = []

url = URL("http://www.mdbg.net/chindict/chindict.php?page=radicals")
dom = DOM(url.download(cached=True))

radElements = dom('a.rad')

for rad in radElements:
    radicals.append(rad.content)
    words = []
    wordUrl = URL("http://www.mdbg.net/chindict/" + rad.attrs["href"])
    wordDom = DOM(wordUrl.download(cached=True))
    wordTable = wordDom.by_class("results")

    for word in wordTable[0].by_tag("span"):
        words.append(word.content)

    chindict[rad.content] = words

with open('chindict.js', 'w') as outfile:
    json.dump(radicals, outfile)
    json.dump(chindict, outfile)

