import requests
import json
from lxml import html

def get_page_links(text):
    root = html.fromstring(text)
    links = root.xpath("//table[@id=\"tblPrjSummary\"]/tr[@class=\"prjSearchResult\"]/td[@class=\"tdPrjRef\"]/a/@href")
    return ["http://www.itf.gov.hk/l-eng/" + link for link in links] 

def get_page_detail(text, tech_area):
    root = html.fromstring(text)
    sels = root.xpath("//table[@id=\"tblPrjProfile\"]/tr")
    count = len(sels)
    d = {"category": tech_area}
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
    for i in range(1, total_pages):
        print "Page:%d" % (i)
        formdata = {"techArea": value, 'token': token, 'submit': 'Search', 'page_no': str(i)}
        page_response = requests.post('http://www.itf.gov.hk/l-eng/Prj_SearchResult.asp', data=formdata, cookies=response.cookies)
        links = get_page_links(page_response.text)
        for link in links:
            detail_response = requests.get(link, cookies=response.cookies)
            details.append(get_page_detail(detail_response.text, category)) 
            print json.dumps(details[-1])
    print "Number of Projects %d" % (len(details))
    output[category] = details

print "Writing File..."
f = open("projects_uncleansed.json", "w")
f.write(json.dumps(output))
f.close()
