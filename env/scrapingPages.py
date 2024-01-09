import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin

def getHtml(base_url, page):
      headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    
      url = base_url + page
    
      response = httpx.get(url, follow_redirects = True)
      html = HTMLParser(response.text)

      if html.css_first('div[data-supermodelid]') is None:
            print("Dernière Page: Fin du Scrapping")
            return False
        
      return html

def parseUrls(html):
      produits = html.css('div[data-supermodelid]')
      for produit in produits:
            urljoin('https://www.decathlon.fr', produit.css_first(' a[class*="product-model-link"]').attributes['href'])
      print(len(produits))

def main():
      base_url = "https://www.decathlon.fr/tous-les-sports/velo-cyclisme/velos"
      for x in range(0, 100):
            
            suffixe = f"?from=" + f"{x * 40}&size=40"
            url = base_url + suffixe
            
            print(f"Go to Web Page:{url}?from="+ f"{x * 40}&size=40")
            html = getHtml(base_url, page=suffixe)
            if html is False:
                  break
            
            parseUrls(html)

if __name__=="__main__":
      main()