import re

import urllib.request
import bs4

class Product():

    def __init__(self, product_url):
        self.product_url = product_url
        self.total_ratings = False
        self.total_reviews = False
        self.num_pages = False
        self.ratings = False
        self.average_ratings = False
        self.image = False
        self.product_name = False
        try:
            self.product_id = re.findall('/([A-Z0-9]{10})', self.product_url)[0]
        except IndexError:
            self.product_id = False
        else:
            print(f'searching for product id {self.product_id}')
            self.url = f'https://www.amazon.in/product-reviews/{self.product_id}/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber='

            self.total_ratings, self.total_reviews, self.num_pages, self.ratings, self.average_ratings = Product.get_review_details(self.url + str(1))
            self.product_link, self.image, self.product_name = self.get_product_details()


    def pagination(self, page_no):
        print(f'url={self.url + str(page_no)}')
        soup = Product.get_soup(url=self.url + str(page_no))
        
        reviews_html = soup.find_all('span', class_='a-size-base review-text review-text-content')
        review_regex = re.compile(r'(?:<span>)(.*)(?:</span>)')
        reviews = []
        if len(reviews_html) == 0:
            return False
        for i in reviews_html:
            reviews.append(review_regex.findall(str(i)))
        
        return reviews
    
    def get_all_reviews(self):
        i = 1
        reviews = []
        print("Total number of pages: ", self.num_pages)
        while True: 
            print(f'getting reviews from page no. {i}')
            page_reviews = self.pagination(i)
            if page_reviews:    
                reviews.extend(page_reviews)
                i+=1
            else:
                continue
            if i == self.num_pages:
                break

        reviews = [i[0] if len(i) != 0 else '' for i in reviews]
        
        return reviews

    @staticmethod
    def get_soup(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # create a request object with the URL and headers
        req = urllib.request.Request(url=url, headers=headers)

        # make a GET request to the URL and get the HTML content
        response = urllib.request.urlopen(req)
        html_code = response.read()

        soup = bs4.BeautifulSoup(html_code,'html.parser')
        return soup       

    def get_product_details(self):
        img = ''
        i = 1
        url = f'https://www.amazon.in/dp/{self.product_id}/'
        while not img:
            soup = Product.get_soup(url)
            
            img = soup.find('div', class_='imgTagWrapper')
            name = soup.find('span', class_='a-size-large product-title-word-break')
            if i == 100:
                break
            i+=1
        if img:
            img = img.img['src']
        if name:
            name = name.text.strip()
        return url, img, name

    @staticmethod
    def get_review_details(url):

        soup = Product.get_soup(url=url)
        # print(url)
        # ratings_reviews = soup.find('div', class_='a-row a-spacing-base a-size-base').text.strip().replace(',', '').split()
        ratings_reviews = soup.find('div', class_='a-row a-spacing-base a-size-base')
        # print(f'{ratings_reviews=}')
        i  = 1
        while not ratings_reviews:
            # print(f'{ratings_reviews=}')
            print(f'trying for reviews {i}')
            soup = Product.get_soup(url=url)
            # print(f'{soup=}')
            ratings_reviews = soup.find('div', class_='a-row a-spacing-base a-size-base')

            i+=1
            if i==50:
                total_ratings =  False
                total_reviews =  False
                num_pages = False
                break
        # print(soup)
        if ratings_reviews:
            ratings_reviews = ratings_reviews.text.strip().replace(',', '').split()
            total_ratings = int(ratings_reviews[0])
            total_reviews = int(ratings_reviews[3])
            num_pages = (total_reviews // 10) + 1 if total_reviews%10 != 0 else (total_reviews // 10)
        

        ratings_html = soup.find_all('div', attrs={'class': 'a-meter'})
        # print(ratings_html)

        i=1
        while not ratings_html:
            print(f'trying for ratings {i}')
            soup = Product.get_soup(url=url)
            ratings_html = soup.find_all('div', attrs={'class': 'a-meter'})
            i+=1
            if i==50:
                break

        ratings_per = []
        for rating in ratings_html:
            ratings_per.append(int(re.findall(r'[0-9]+',str(rating).split()[1])[0]))
        ratings = {f'{5-i} star': j for i, j in enumerate(ratings_per)}

        average_rating = soup.find('span', attrs={'data-hook': 'rating-out-of-text'})
        
        i = 1
        while not average_rating:
            print(f'trying for average ratings {i}')
            soup = Product.get_soup(url=url)
            average_rating = soup.find('span', attrs={'data-hook': 'rating-out-of-text'})
            i+=1
            if i==50:
                average_rating = False
                break

        if not ratings:
            ratings = False

        if average_rating:
            average_rating = average_rating.text
        else:
            average_rating = False
        

        return total_ratings, total_reviews, num_pages, ratings, average_rating


    def __str__(self):
        try:
            return self.url
        except AttributeError:
            return 'No product found'

    
    def __repr__(self):
        try:    
            return self.url
        except AttributeError:
            return 'No product found'
    