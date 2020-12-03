from bs4 import BeautifulSoup
import urllib.request
def main():
    url = "https://pypi.fury.io/sKv8PCZngFJ-g_oEqjfc/iotile/prodtools-core"
    data = urllib.request.urlopen(url).read()
    # print(data)
    soup = BeautifulSoup(data, features="html.parser")
    for link in soup.find_all('a'):
        print(link.contents[0])
if __name__ == "__main__":
    main()