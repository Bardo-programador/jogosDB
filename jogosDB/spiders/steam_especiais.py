import scrapy
from scrapy_splash import SplashRequest
from jogosDB.items import JogosdbItem
import json
from scrapy.selector import Selector
class SteamEspeciaisSpider(scrapy.Spider):
    name = "steam_especiais"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&ignore_preferences=1&supportedlang=brazilian&snr=1_7_7_2300_7&specials=1&infinite=1"]
    ##Descomentar caso esteja usando o splash e tenha o docker instalado e ativado com:
    ## docker run -p 8050:8050 scrapinghub/splash
    # def start_requests(self):
    #     url = 'https://store.steampowered.com/search/?specials=1&ndl=1'
    #     yield SplashRequest(url, self.parse, args={'wait': 5})
    custom_settings = {
        'FEEDS' : {'dados/steam.jsonl': {'format' : 'jsonlines',
                                         "overwrite": True}},
       }
    
    def parse(self, response):
        # Pega os dados através de uma requisição json
        pagina = dict(response.json()) ## Pega o codigo json da pagina
        total_jogos = pagina['total_count'] #Pega o total de jogos
        start = pagina['start'] #Pega o valor de start
        if int(start) == 0:
            ## Aqui é feito o pre-processamento para pegar todos os links das páginas para otimizar a busca
            for i in range(50, int(total_jogos), 50): 
                yield response.follow(f"https://store.steampowered.com/search/results/?query&start={i}&count=50&dynamic_data=&sort_by=_ASC&ignore_preferences=1&supportedlang=brazilian&snr=1_7_7_2300_7&specials=1&infinite=1")
        seletor = Selector(text = pagina['results_html']) ## Transforma o codigo html em um objeto do scrapy
        nomes = seletor.css(".title::text").getall() ##Pega os nomes de todos osjogos
        precos = seletor.css(".discount_final_price::text").getall() ##Pega o preço de todos os jogos
        links = seletor.css("a::attr(href)").getall() ##Pega o link de todos os jogos
        for nome, preco, link in zip(nomes, precos, links): ## Itera sobre as listas
            jogo = JogosdbItem() ##Instancia o item jogo
            # Salva os dados nos campos do item
            jogo['name'] = nome
            jogo['price'] = preco
            jogo['link'] = link
            yield jogo ## Retorna o item