import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

class MercadoLibreItem(Item):
    modelo = scrapy.Field()
    precio = scrapy.Field()
    condicion = scrapy.Field()
    vendedor = scrapy.Field()


class MercadoLibreCrawler(CrawlSpider):
    name = "MiPrimerCrawler"
 
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT' : 20 #para limitar la cantidad de datos extraidos
    }

    download_delay=1
    allowed_domains = ['listado.mercadolibre.com.ar','www.mercadolibre.com.ar']
    start_urls= ["https://listado.mercadolibre.com.ar/consolas"]


    #reglas para ir saltando de una pagina a otra
    rules = (
     
    #Paginacion
    Rule(
        
        LinkExtractor(allow = r'/consolas_Desde_'), follow = True
        ),

    #Detalle de productos
    Rule(

        LinkExtractor(allow=(), restrict_xpaths= ('//div[@class="ui-search-item__group ui-search-item__group--title"]/a')), 
        follow=False, callback= 'parse_item'
        
        ),
    )

    def parse_items(self, response):
        item = ItemLoader(MercadoLibreItem(), response)

        item.add_xpath('modelo', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('precio', '/html/body/main/div[2]/div[4]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div[1]/span/span[3]/text()')
        item.add_xpath('condicion', '//span[@class="ui-pdp-subtitle"]/text()')
        #item.add_xpath('vendedor', '//span[@class="ui-pdp-color--BLUE ui-pdp-family--REGULAR"]/text()')
        item.add_xpath('vendedor', '//*[contains(@class, "ui-pdp-color--BLUE ui-pdp-family--REGULAR")]/text()')

        yield item.load_item()


