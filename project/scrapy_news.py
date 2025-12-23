import scrapy

class QuantumNewsSpider(scrapy.Spider):
    name = "quantum_news"
    start_urls = ["https://news.mit.edu/2025/mit-engineers-advance-toward-fault-tolerant-quantum-computer-0430"]

    # def parse(self, response):
    #     for article in response.css("div.latest-head"):
    #         yield {
    #             "title": article.css("a::text").get(),
    #             "link": response.urljoin(article.css("a::attr(href)").get()),
    #         }
    # def parse(self, response):
    #     for article in response.css("div.latest-head"):
    #         title = article.css("a::text").get()
    #         link = response.urljoin(article.css("a::attr(href)").get())
    #         print(f"Title: {title}, Link: {link}")  # Debugging output
    #         yield {"title": title, "link": link}
    def parse(self, response):

      print(response.text)  # Print the raw HTML to debug