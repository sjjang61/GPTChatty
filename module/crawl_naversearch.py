
import requests
from bs4 import BeautifulSoup
import time
from module.cache_utils import CacheManager

## https://velog.io/@sh97818/Crawling-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%89%B4%EC%8A%A4-%EB%B3%B8%EB%AC%B8-%ED%81%AC%EB%A1%A4%EB%A7%81
crawl_cache_manager = CacheManager('url')

def get_contents( url : str ) -> dict:
    cache_data = crawl_cache_manager.get_cache( url )
    if cache_data != None:
        return cache_data

    cache_data = crawl_page( url )
    crawl_cache_manager.set_cache( cache_data )
    return cache_data

def crawl_page( url : str ) -> dict:
    response = requests.get( url )
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("div.info_group")
    crawl_data = { 'url' : '', 'title' : '', 'content' : ''}

    for article in articles:
        links = article.select("a.info")
        if len(links) >= 2:
            url = links[1].attrs["href"]
            response = requests.get(url, headers={'User-agent': 'Mozila/5.0'})      # to avoid error use headers
            html = response.text                                                    # for each url get html
            soup = BeautifulSoup(html, "html.parser")                               # for each html make soup

            # separation
            if "entertain" in response.url:                                         # to avoid redirection error
                title = soup.select_one(".end_tit")                                 # get the title
                content = soup.select_one("#articeBody")                            # get the body
            else:
                title = soup.select_one(".media_end_head_headline")                 # get the title
                content = soup.select_one("#dic_area")                              # get the body

            # print("========LINK========\n", url)
            # print("========TITLE========\n", title.text.strip())
            # print("========BODY========\n", content.text.strip())
            crawl_data['url'] = url
            crawl_data['title'] = title.text.strip()
            crawl_data['content'] = content.text.strip()

            print("======== [CRWALING_BEGIN] ========" )
            print( f"title = {crawl_data['title']}, content = {crawl_data['content']}")
            print("========  [CRWALING_END]  ========")
            time.sleep(0.3)
            break

    return crawl_data


# content = get_contents( "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%B8%94%EB%9E%99%ED%95%91%ED%81%AC&oquery=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&tqi=hyYPFlprvmsss4UxVAhssssssg4-385087")
# print( content )