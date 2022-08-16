# ptt-crawler
This project scrapes/crawls post content and comments from [PTT](https://term.ptt.cc/) website, and implements [neural CKIP Chinese NLP tools](https://github.com/ckiplab/ckip-transformers) on the scraped data.

## **Documentation**
### 1. Installation
- Python version: 3.7.5 (due to CKIP)
- Clone repository
  ```bash
  git clone git@github.com:Retr0327/ptt-crawler.git
  ```
- Install Requirement
  ```bash 
  cd scraptt && pip install -r requirement.txt      
  ```


### 2. Start the crawler
There are three main ways to run the crawler:
- scrap all the posts of a board:
  ```bash
  scrapy crawl ptt_post -a boards=Soft_Job -a all=True
  ```
- scrap all the posts of a board from a year in the past:
  ```
  scrapy crawl ptt_post -a boards=Soft_Job -a since=2021
  ```
- scrap the posts of a board based on html indexes:
  ```
  scrapy crawl ptt_post -a boards=Soft_Job -a index_from=1715 -a index_to=1718 
  ```

> if you want to scrap multiple boards, simply run: 
> ```
> -a boards=board_1,board_2
> ``` 
> For exampel, the following command scrapes all the posts from `Soft_Job` and `Baseball` boards.
> ```
> scrapy crawl ptt_post -a boards=Soft_Job,Baseball -a all=True
> ```

