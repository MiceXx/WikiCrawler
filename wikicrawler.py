import time
import urllib
import bs4
import requests

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    articleLink = None

    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            articleLink = element.find("a", recursive=False).get('href')
            break

    if not articleLink:
        return

    firstLink = urllib.parse.urljoin('https://en.wikipedia.org/', articleLink)

    return firstLink

def continue_crawl(search_history, target_url, max_steps=25):
    print("working...")
    l = len(search_history)
    if search_history[-1] == target_url:
        print("Found target:" + target_url)
        return False
    elif l > max_steps:
        print("Reached max number of iterations")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("Encountered a loop:" + search_history[-1])
        return False
    return True

articleChain = [start_url]

while continue_crawl(articleChain, target_url):
    print(articleChain[-1])

    firstLink = find_first_link(articleChain[-1])
    if not firstLink:
        print("something Went wrong")
        break

    articleChain.append(firstLink)

    #time.sleep(1)