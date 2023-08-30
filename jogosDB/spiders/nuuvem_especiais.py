import scrapy
from scrapy_splash import SplashRequest
import json
from jogosDB.items import JogosdbItem
geraJson = lambda x: json.loads(x)

class NuuvemEspeciaisSpider(scrapy.Spider):
    name = "nuuvem_especiais"
    allowed_domains = ["www.nuuvem.com"]
    start_urls = ["https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc/page/1"]
    ##Descomentar caso esteja usando o splash e tenha o docker instalado e ativado com:
    ## docker run -p 8050:8050 scrapinghub/splash
    # def start_requests(self):
    #     url = 'https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc'
    #     yield SplashRequest(url, self.parse, args={'wait': 5})
    custom_settings = { 
        'FEEDS' : {'dados/nuuvem.jsonl': {'format' : 'jsonlines', 'overwrite' : True }},
     }
    
    def parse(self, response):
        
        pagina_atual = response.css("#catalog > div:nth-child(3) > div.products-items > footer > nav > a.pagination--item.pagination--item-active::text").get()
        if int(pagina_atual) == 1:
            total_paginas = response.css("#catalog > div:nth-child(3) > div.products-items > footer > nav > a:nth-child(8)::text").get() ## Pega o total de paginas
            for i in range(2, int(total_paginas)+1): ## Itera sobre as paginas
                yield response.follow(f"https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc/page/{i}")
        tabela = response.css("#catalog > div:nth-child(3) > div.products-items > div > div div") ##Pega uma lista de divs 
        for jogos in tabela:
            jogo = JogosdbItem()            
            nome = jogos.css("div.product-card--grid > div > a > div.product-card--content > div > h3::text").get()
            if nome is None:
                continue
            preco = jogos.css("div.product-card--grid > div > a > div.product-card--footer > div::attr(data-price)").get()
            preco = geraJson(preco)
            link = jogos.css("div.product-card--grid > div > a::attr(href)").get() ## Pegando o link do jogo
            jogo['name'] = nome ## Pegando o nome do jogo
            jogo['price'] = preco['v']/100 ## Pegando o preço do jogo e dividindo por 100 para ficar
            jogo['link'] = link
            yield jogo
        # next_page_url = response.css('#catalog > div:nth-child(3) > div.products-items > footer > nav > a.pagination--action.pagination--action-right::attr(href)').get()
        # if next_page_url:
        #     next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)
#catalog > div:nth-child(3) > div.products-items > div > div > div:nth-child(2) > div > a > div.product-card--content > div > h3
