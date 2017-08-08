import scrapy
import json
from scrapy_splash import SplashRequest

script = """
function main(splash)
    splash:set_result_content_type("text/html; charset=utf-8")
    assert(splash:go(splash.args.url))
    splash:wait(5)
    return splash:html()
end
"""

class WhoscoredspiderSpider(scrapy.Spider):
    name = "whoscoredspider"
    allowed_domains = ["qq.com"]
    start_urls = [
        "https://www.ospe.on.ca/courses#507/PE402-0717"
    ]

    def start_requests(self):
        for url in self.start_urls:
            print("url ===>",url)
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={
                    'lua_source': script
                }
            )

    def parse(self, response):
        print("parsing from here ++++++")
        print ("response body=====>",response.body)

