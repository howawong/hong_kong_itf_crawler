import requests
import json
from lxml import html
from multiprocessing import Pool 
import signal

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def get_page_links(text):
    root = html.fromstring(text)
    links = root.xpath("//table[@id=\"tblPrjSummary\"]/tr[@class=\"prjSearchResult\"]/td[@class=\"tdPrjRef\"]/a/@href")
    return ["http://www.itf.gov.hk/l-eng/" + link for link in links] 

def get_page_detail(pair):
    link, cookies = pair
    detail_response = requests.get(link, cookies=cookies)
    root = html.fromstring(detail_response.text)
    sels = root.xpath("//table[@id=\"tblPrjProfile\"]/tr")
    count = len(sels)
    d = {}
    if count > 0:
        for sel in sels:
            key = ""
            for text in sel.xpath("td[@class=\"prjProfile1\"]//text()"):
                key = key + text
            key = key.strip()

            value = ""
            values = [v.strip() for v in sel.xpath("td[@class=\"prjProfile2\"]//text()")]
            value = "".join(values).strip()
            d[key] = value
        return d
    else:
        print "fucked %s "% (response.meta['title'])
        raise Exception("No record found")

url = "http://www.itf.gov.hk/l-eng/Prj_Search.asp?code=108"
response = requests.get(url)
root = html.fromstring(response.text)
token = root.xpath("//input[@name=\"token\"]/@value")[0]
print token
print response.cookies
options = root.xpath("//select[@id=\"techArea\"]/option")
output = {}
for option in options:
    category = option.xpath("text()")[0]
    value = option.xpath("@value")[0]
    print category + " [" + value  + "]"
    formdata = {"techArea": value, 'token': token, 'submit': 'Search'}
    page_response = requests.post('http://www.itf.gov.hk/l-eng/Prj_SearchResult.asp', data=formdata, cookies=response.cookies)
    root = html.fromstring(page_response.text)
    total_pages = int("".join([x.strip() for x in root.xpath("//table[@id=\"prjSearchPageTable\"]//tr[@class=\"prjSearchResult\"]/td//text()")]).split(" of ")[1].strip())
    details = []
    for i in range(1, total_pages + 1):
        print "Page:%d" % (i)
        formdata = {"techArea": value, 'token': token, 'submit': 'Search', 'page_no': str(i)}
        page_response = requests.post('http://www.itf.gov.hk/l-eng/Prj_SearchResult.asp', data=formdata, cookies=response.cookies)
        links = get_page_links(page_response.text)
        p = Pool(10, init_worker)
        try:
            details_per_page = p.map(get_page_detail, [(link, response.cookies) for link in links])
            for detail in details_per_page:
                print json.dumps(detail)
            details = details + details_per_page
        except KeyboardInterrupt:
            p.terminate()
            p.join()
        finally:
            p.close()
    print "Number of Projects %d" % (len(details))
    output[category] = details

print "Writing File..."
f = open("projects_uncleansed.json", "w")
f.write(json.dumps(output))
f.close()
