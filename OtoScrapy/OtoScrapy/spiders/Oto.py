import scrapy
import csv
import pymongo
import os
import time
import json

class OtoSpider(scrapy.Spider):
    name = "Oto"
    allowed_domains = ["https://bonbanh.com/"]
    start_urls = [f"https://bonbanh.com/oto/page,{i}" for i in range(1, 52)]
    def __init__(self, *args, **kwargs):
        super(OtoSpider, self).__init__(*args, **kwargs)
        # Thiết lập kết nối tới MongoDB
        econnect = str(os.environ.get('Mongo_HOST', 'localhost'))
        self.client = pymongo.MongoClient(f'mongodb://{econnect}:27017')
        self.db = self.client["oto_db"]  # Tạo hoặc kết nối tới database oto_db
        self.collection = self.db["oto_collection"]  # Tạo hoặc kết nối tới collection oto_collection


    def parse(self, response):
       
        for oto in response.css('li.car-item'):
            
            phonenumber = oto.css('div.cb7::text').getall()
            sellername = oto.css('div.cb7 b::text').getall()
            address = oto.css('div.cb7 span::text').getall()
            status = oto.css('div.cb1::text').getall()
            year = oto.css('div.cb1 b::text').getall()
            code = oto.css('div.cb5 span.car_code::text').getall()
            carname = oto.css('div.cb2_02 h3::text').getall()
            price = oto.css('div.cb3 b::text').getall()
            city = oto.css('div.cb4 b::text').getall()
            parameter = oto.css('div.cb6_02::text').getall()
            content = oto.css('div.cb6_02 p::text').getall(),
            data={
                'phonenumber' : phonenumber,
                'sellername' : sellername,
                'address' : address,
                'status' : status,
                'year' : year,
                'code' : code,
                'carname' : carname,
                'price' : price,
                'city' : city,
                'parameter' : parameter,
                'content' : content,
            }        

            self.collection.insert_one(data)
            time.sleep(0.1)
            # Yield dữ liệu (cũng có thể lưu vào file nếu cần)
            yield data
        with open('OOO.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def close(self, reason):
        # Đóng kết nối MongoDB khi hoàn thành
        self.client.close()

