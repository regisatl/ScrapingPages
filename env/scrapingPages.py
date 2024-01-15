from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from urllib.parse import urljoin
import pandas as pd
import httpx
import time

@dataclass
class Item:
      name: str | None
      Marque: str | None
      Référence: str | None
      Prix: str | None
      Avis: str | None

def getHtml(base_url, **kwargs):
      headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
      
      if kwargs.get("page"):
            url = base_url + kwargs.get("page")
      else:
            url = base_url
    
      response = httpx.get(url, headers=headers, follow_redirects = True)
      html = HTMLParser(response.text)

      if kwargs.get("page") and html.css_first('div[data-supermodelid]') is None:
            print("Dernière Page: Fin du Scrapping")
            return False
      
      return html

def parseUrls(html):
      produits = html.css('div[data-supermodelid]')
      for produit in produits:
            yield(urljoin('https://www.decathlon.fr', produit.css_first(' a[class*="product-model-link"]').attributes['href'] ))

def extractData(html, sel):
      try:
            data = html.css_first(sel).text().strip()
            return data
      except AttributeError:
            return None

def parseDetailedPages(html):
      newItem = Item(
            Nom = extractData(html, 'h1'),
            Marque = extractData(html, 'a[aria-label^="Voir plus de produits de la marque]'),
            Référence = extractData(html, 'span[class^="current-selected-model"]'),
            Prix = extractData(html, 'span[class^="price_size--large"]'),
            Avis = extractData(html, 'button[class^="review-link"]'),
      )
      return asdict(newItem)
      
def cleanData(produits):
      df = pd.DataFrame(columns=produits[0].keys())
      for produit in produits:
            length = len(df)
            df.loc[length] = produit
      df["Référence"] = df["Référence"].str.replace("Ref. :", "", regex=False).str.strip()
      df["Avis"] = df["Avis"].str.extract('(\d*\)')

def main():
      produits = []
      base_url = "https://www.decathlon.fr/tous-les-sports/velo-cyclisme/velos"
      
      for x in range(0, 1):
            suffixe = f"?from=" + f"{x * 40}&size=40"
            url = base_url + suffixe
            print(f"Go to Web Page:{url}?from="+ f"{x * 40}&size=40")
            html = getHtml(base_url, page=suffixe)
            if html is False:
                  break
            time.sleep(1)
            
            urls = parseUrls(html)
            for url in urls[:3]:
                  print(f"Click item : {url}")
                  html = getHtml(url)
                  produits.append(parseDetailedPages(html))
                  print(f"ExtractData: {produits[-1]} ")
                  time.sleep(1)
            
            cleanData(produits)

if __name__=="__main__":
      main()