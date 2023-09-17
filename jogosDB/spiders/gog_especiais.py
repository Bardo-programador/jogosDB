import scrapy
from jogosDB.items import JogosdbItem

class GogEspeciaisSpider(scrapy.Spider):
    name = "gog_especiais"
    allowed_domains = ["www.gog.com"]
    start_urls = ["https://www.gog.com/en/games?discounted=true&hideDLCs=true"]
    custom_settings = {'FEEDS' : {'dados/gog.jsonl': {'format' : 'jsonlines',
                                         "overwrite": True}}
                                         }
    def parse(self, response):
        pagina_atual = response.css("#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > paginated-products-grid > pagination-template > div > div:nth-child(2) > pagination-input > input::attr(value)").get()
        if pagina_atual == "1":
            numero_paginas = int(response.css("#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > paginated-products-grid > pagination-template > div > div:nth-child(8) > button > span::text").get())
            for i in range(2, numero_paginas+1):
                print("Carregou a página ", i)
                yield response.follow(f"https://www.gog.com/en/games?discounted=true&hideDLCs=true&page={i}")
        tabela_jogos = response.css("#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > paginated-products-grid > div > product-tile")
        for jogo in tabela_jogos:
            Jogo = JogosdbItem()
            Jogo['link'] = jogo.css("product-tile > a::attr(href)").get()
            Jogo['name'] = jogo.css("product-tile > a > div.product-tile__info > div.product-tile__title > product-title > span::text").get()
            Jogo['price'] = jogo.css("product-tile > a > div.product-tile__info > div.product-tile__footer > div > product-price > price-value > span.final-value::text").get()
            yield Jogo