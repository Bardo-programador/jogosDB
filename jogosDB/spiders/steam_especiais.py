import scrapy
from scrapy_splash import SplashRequest
from jogosDB.items import JogosdbItem

class SteamEspeciaisSpider(scrapy.Spider):
    name = "steam_especiais"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?supportedlang=brazilian&specials=1&ndl=1"]
    ##Descomentar caso esteja usando o splash e tenha o docker instalado e ativado com:
    ## docker run -p 8050:8050 scrapinghub/splash
    # def start_requests(self):
    #     url = 'https://store.steampowered.com/search/?specials=1&ndl=1'
    #     yield SplashRequest(url, self.parse, args={'wait': 5})
    custom_settings = {
        'ITEM_PIPELINES' : {
            'jogosDB.pipelines.SteamWriterPipeline': 400
             ,
       }
    }
    def parse(self, response):
        tabela_jogos = response.css("#search_resultsRows a") ## Pegando a tag que contem a lista de jogos da página
        indice = 0
        for jogos in tabela_jogos: ## Iterando sobre a lista de jogos através dos links
            # Instancia o item jogo
            jogo = JogosdbItem()
            # Coleta o nome, preco e link nos nas tags
            jogo['name'] = jogos.css(f"a > div.responsive_search_name_combined > div.col.search_name.ellipsis > span.title::text").get(),
            jogo['price'] = (int(jogos.css(f"a > div.responsive_search_name_combined > div.col.search_price_discount_combined::attr(data-price-final)").get())/100),            
            jogo['link'] = jogos.css("a::attr(href)").get()
            yield jogo