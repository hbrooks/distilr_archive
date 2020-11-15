FROM python:3.7

WORKDIR /usr/src/api_distilr_news

# Copy these before the source code to take advantage of cacheing container layers.
RUN mkdir /usr/src/api_distilr_news/ssl
# COPY shared/ssl/distilr_news.csr /usr/src/api_distilr_news/ssl/distilr_news.csr
# COPY shared/ssl/distilr_news.key /usr/src/api_distilr_news/ssl/distilr_news.key
COPY api_distilr_news/requirements.txt /usr/src/api_distilr_news/requirements.txt

RUN pip install -r /usr/src/api_distilr_news/requirements.txt

RUN mkdir /usr/src/api_distilr_news/api_distilr_news
COPY api_template/api_template/ /usr/src/api_distilr_news/api_distilr_news
COPY api_distilr_news/ /usr/src/api_distilr_news
