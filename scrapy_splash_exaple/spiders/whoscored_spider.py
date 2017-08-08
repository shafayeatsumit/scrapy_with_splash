# -*- coding: utf-8 -*-

import scrapy
import json
from scrapy_splash import SplashRequest

script = """
function main(splash)
    assert(splash:go(splash.args.url))
    local get_info = splash:jsfunc([[
    function () {
    var course_detail = document.getElementById('note').innerHTML;
    return course_detail;
    }
    ]])    
    function wait_for(splash, condition)
        while not condition() do
            splash:wait(0.05)
        end
    end

    wait_for(splash, function()
        return splash:evaljs("document.getElementById('note') !== null")
    end)
    return {
        data = get_info(),
        contact_info = splash:evaljs("document.getElementById('contact').innerText"),
        title =  splash:evaljs("document.getElementsByClassName('eventTitle')[0].innerText"),
        event_date = splash:evaljs("document.getElementById('startEndDates').innerText"),
        location = splash:evaljs("document.getElementById('location').innerText")
    }
end
"""

class WhoscoredspiderSpider(scrapy.Spider):
    name = "whoscoredspider"
    start_urls = [
        "https://www.ospe.on.ca/courses#507/PE402-0717"
    ]

    def start_requests(self):
        for url in self.start_urls:
            print("url ===>",url)
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={
                    'lua_source': script,
                    'timeout': 90
                }
            )

    def parse(self, response):
        rs = response.body.decode('unicode_escape')
        print(rs)

    

