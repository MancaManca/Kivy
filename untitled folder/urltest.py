# import json
#
# import urllib3
# from kivy.network.urlrequest import UrlRequest
#
# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
# from kivy.network.urlrequest import UrlRequest
# import requests as request
# import ujson
#
# ujson.dumps([{"key": "value"}, 81, True])
# '[{"key":"value"},81,true]'
# ujson.loads("""[{"key": "value"}, 81, true]""")
# # [{u'key': u'value'}, 81, True]
#

url = "http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces"
# # http = urllib3.PoolManager()
# r = request.get(url)
# r = ujson.dumps(r, encode_html_chars=False  , ensure_ascii=True,escape_forward_slashes=False,indent=4)
# # aa = json.detect_encoding(r.content)
# # r = r.text
# # r = json.loads(r)
# # aa = json.dumps(r,sort_keys=True, indent=4)
# t = ujson.loads(r)
# # t = json.loads(r)
# # print(json.dumps((r),sort_keys=True, indent=4))
# print(t[1])
# # class MainScreen(FloatLayout):
# #     def __init__(self, **kwargs):
# #         super(MainScreen, self).__init__(**kwargs)
# #         search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
# #         UrlRequest(search_url, on_failure=self.got_fail,
# #                        on_error=self.got_error, debug=True,
# #                        on_success=self.got_success,
# #                        on_redirect=self.got_redirect)
# #
# #     def got_success(self, req, *args):
# #         print("got success {0}".format(req.result))
# #
# #     def got_error(self, req,  *args):
# #         print("got error {0}".format(req.url))
# #
# #     def got_fail(self, req, *args):
# #         print("got fail {0}".format(req.url))
# #
# #     def got_redirect(self, req, *args):
# #         print("got redirect {0}".format(req.url))
# #
# #
# # class App(App):
# #     def build(self):
# #         return MainScreen()
# #
# # if __name__ == "__main__":
# #     App().run()
# # print('req')
# # # req = UrlRequest(search_url)
# # print('req')
# #
# # #
# # # def pr(resp_status):
# # #     print('Tits{}'.format(resp_status))
# #
# #
# # # print(UrlRequest(search_url, on_success=pr))
# # req = UrlRequest(search_url)
# # print(req.resp_status)
# # print(req.is_finished)
# # print(req.error)
# # # req.wait(1)
# # # while req.resp_status is None:
# # #     t=0
# # #     print('1')
# # #     req.wait(3)
# # #
# # # # req.wait(3)
# # source_code = req.result
# # print('{}'.format(source_code))
# # eur = source_code[1833:1841]
# #
# # conv_eur = str(eur)
# # print('{}'.format(conv_eur))
# # dol = source_code[6338:6346]
# # conv_dol = str(dol)
# # print('{}'.format(conv_dol))
# # troskovi = {
# #     'porez': 22400,
# #     'stan': float(eur) * 225,
# #     'osiguranje': 3000,
# #     'kuca': 20000,
# #     'racuni': 10000,
# # }
# # tr = sum(troskovi.values())
# #
# # plata = float(float(dol) * 1350)
# #
# # ostatak = float(float(dol) * 1350) - float(tr)
# # print(conv_dol)
# # print(conv_eur)
# # print(tr)
# # print(plata)
# # print(ostatak)


import requests as request

from pyparsing import *

anchorStart, anchorEnd = makeHTMLTags("td")
# bla = m
# read HTML from a web page
serverListPage = request.get(url)
htmlText = serverListPage.text

anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd

d = {}
l = []
for tokens, start, end in anchor.scanString(htmlText):
    # print(tokens.body, '->', tokens.href)
    d[tokens.body] = tokens.href
    l.append(tokens.body)
for i in d:
    print('{} {}\n'.format(i,d[i]))
l.pop(0)
l.pop(151)
l.pop(150)
baba = None
deda = None
# l.remove(1)
for i, j in enumerate(l):
    if j == 'EUR':
        print(i)
        baba = i+2
    if j == 'USD':
        print(i)
        deda = i+2
print(l)
print(l[baba])
print(l[deda])
# # URL extractor
# # Copyright 2004, Paul McGuire
# from pyparsing import Literal,Suppress,CharsNotIn,CaselessLiteral,\
#         Word,dblQuotedString,alphanums,SkipTo,makeHTMLTags
# import urllib
# import pprint
#
# # Define the pyparsing grammar for a URL, that is:
# #    URLlink ::= <a href= URL>linkText</a>
# #    URL ::= doubleQuotedString | alphanumericWordPath
# # Note that whitespace may appear just about anywhere in the link.  Note also
# # that it is not necessary to explicitly show this in the pyparsing grammar; by default,
# # pyparsing skips over whitespace between tokens.
# linkOpenTag,linkCloseTag = makeHTMLTags("a")
# link = linkOpenTag + SkipTo(linkCloseTag).setResultsName("body") + linkCloseTag.suppress()
#
# # Go get some HTML with some links in it.
# serverListPage = urllib.urlopen( "http://www.google.com" )
# htmlText = serverListPage.read()
# serverListPage.close()
#
# # scanString is a generator that loops through the input htmlText, and for each
# # match yields the tokens and start and end locations (for this application, we are
# # not interested in the start and end values).
# for toks,strt,end in link.scanString(htmlText):
#     print toks.startA.href,"->",toks.body
#
# # Create dictionary from list comprehension, assembled from each pair of tokens returned
# # from a matched URL.
# pprint.pprint(
#     dict( [ (toks.body,toks.startA.href) for toks,strt,end in link.scanString(htmlText) ] )
#     )
