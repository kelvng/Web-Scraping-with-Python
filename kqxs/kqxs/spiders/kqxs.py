import scrapy
import calendar
import datetime
from scrapy.spiders import CrawlSpider
from ..items import XsktItem
#from kqxs.kqxs.items import KqxsItem


def get_total_date_month(year, month):
    now = datetime.datetime.now()
    total_date = calendar.monthrange(year, month)[1]

    if year == now.year and month == now.month and now.day < total_date:
        return now.day

    return total_date


class kqxs(scrapy.Spider):
    name = "kqxs"
    allowed_domains = ['xskt.com.vn']
    start_urls = []

    month_to_scrap = 9
    year_to_scrap = 2020

    total_date = get_total_date_month(year_to_scrap, month_to_scrap)

    for i in range(1, total_date):
        start_urls.append('https://xskt.com.vn/xsmb/ngay-''{0}-{1}-{2}.html'.format(i, month_to_scrap, year_to_scrap))

    def parse(self, response):
        xs_item = XsktItem()
        tmp_data = {}
        data_resp = scrapy.Selector(response)

        xs_item['xs_info'] = [
            # Thứ
            data_resp.xpath("//table[@class = 'result']/tr[1]/th/b/a[2]//text()").get(),
            # Ngày tháng
            data_resp.xpath("//div[@class='box-ketqua']/h2/a[2]//text()").get()
        ]

        for j in range(2, 12):
            if j == 6 or j == 9:
                pass
            else:
                # Cột các giải từ giải 8 đến giải đặc biệt
                tmp_giai = data_resp.xpath("//table[@class = 'result']/tr[{0}]/td[1]/text()".format(j)).get()
                tmp_data[tmp_giai] = {}
                # Các số trúng thưởng trong cột
                tmp_number = response.xpath("//table[@class = 'result']/tr[{0}]/td[2]//text()".format(j)).getall()
                tmp_data[tmp_giai] = ",".join(tmp_number)

        xs_item['xs_data'] = tmp_data

        yield xs_item