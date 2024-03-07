import requests
from bs4 import BeautifulSoup as bs
import time

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

    def __str__(self):
        return f"{self.text} - {self.author} - {self.tags}"


def main():
    url = 'https://quotes.toscrape.com'
    soup = bs(requests.get(url).content, "html.parser")
    quotes = []

    while True:
        time.sleep(1)
        relative_url = get_next_page(soup)
        if relative_url is None:
            break
        next_page = url + get_next_page(soup)
        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))

    print_answers(quotes)

    return 



def print_answers(quotes: list):
    questions = [
        ("What is the shortest quote?", get_shortest_quote(quotes)),
        ("What is the longest quote?", get_longest_quote(quotes)),
        ("What are the top 10 tags?", get_top_10_tags(quotes)),
        ("What authors have multiple quotes?", get_authors_with_multiple_quotes(quotes))
    ]

    for question, answer in questions:
        print(f"{question} {answer}")
        print("-" * 50)

def get_shortest_quote(quotes: list):
    quote = min(quotes, key=lambda x: len(x.text))
    return len(str(quote)), min(quotes, key=lambda x: len(x.text)).text

def get_longest_quote(quotes: list):
    quote = max(quotes, key=lambda x: len(x.text))
    return len(str(quote)), max(quotes, key=lambda x: len(x.text)).text


def get_top_10_tags(soup: bs):
    tags = {}

    for quote in soup:
        for tag in quote.tags:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
    tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]
    return tags


def get_authors_with_multiple_quotes(quotes: list):
    authors = {}
    for quote in quotes:
        if quote.author in authors:
            authors[quote.author] += 1
        else:
            authors[quote.author] = 1
    authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
    authors = [(author, count)
               for author, count in authors
               if count > 1]
    return authors


def get_next_page(soup: bs):
    next_button = soup.find("li", {"class": "next"})
    if next_button is not None:
        return str(next_button.find("a")["href"])
    else:
        return None
    

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})
    
    quotes_list = []

    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        tags = [tag.text for tag in quote.find_all("a", {"class": "tag"})]
        q = Quote(text, author, tags)
        quotes_list.append(q)

    return quotes_list


if __name__ == '__main__':
    main()