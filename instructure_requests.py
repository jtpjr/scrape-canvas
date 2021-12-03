from requests_html import HTMLSession
import urllib.request
def get_instructure(url, name):
    session = HTMLSession()

    r = session.get(url)

    # this call executes the js in the page
    r.html.render()  

    # retrieves link from source element that is loaded using javascript
    link = r.html.xpath("//source", first=True).attrs["src"]

    # downloads video
    urllib.request.urlretrieve(link, name) 

