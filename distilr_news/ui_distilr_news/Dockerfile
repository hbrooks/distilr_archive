FROM node:12.14.0

WORKDIR /usr/src/ui_distilr_news

RUN mkdir /usr/src/ui_distilr_news/ssl
# COPY ./shared/ssl/distilr_news.csr /usr/src/ui_distilr_news/ssl/distilr_news.csr
# COPY ./shared/ssl/distilr_news.key /usr/src/ui_distilr_news/ssl/distilr_news.key

COPY ./ui_distilr_news/package.json /usr/src/ui_distilr_news/package.json
COPY ./ui_distilr_news/package-lock.json /usr/src/ui_distilr_news/package-lock.json

RUN npm install

EXPOSE 7000

COPY ui_distilr_news/ /usr/src/ui_distilr_news