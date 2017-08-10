# -*- coding: utf-8 -*-

import scrapy
import json
from scrapy_splash import SplashRequest

script_detail_page = """
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

script_first_page = """
function main(splash)
    assert(splash:go(splash.args.url))  
    function wait_for(splash, condition)
        while not condition() do
            splash:wait(0.05)
        end
    end

    wait_for(splash, function()
        return splash:evaljs("document.getElementById('0') !== null")
    end)
    return splash:html()
end
"""
class WhoscoredspiderSpider(scrapy.Spider):
    name = "whoscoredspider"

    def start_requests(self):
        yield SplashRequest(url= 'https://www.ospe.on.ca/courses', 
               callback = self.parse,
               endpoint='execute',
                args={
                    'lua_source': script_first_page,
                    'timeout': 90
                }            
            )

    def parse(self, response):
        print("parsing called ++++++++++++++++++++++++")
        list_of_course = response.xpath('//td/a/@href').extract()
        print (list_of_course)
        print (len(list_of_course))


