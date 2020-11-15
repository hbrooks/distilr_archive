FROM python:3.7

WORKDIR /usr/src/api_word_timelines

# Copy this before the source code to take advantage of cacheing container layers.
RUN mkdir /usr/src/api_word_timelines/ssl
# COPY shared/ssl/distilr_news.csr /usr/src/api_word_timelines/ssl/distilr_news.csr
# COPY shared/ssl/distilr_news.key /usr/src/api_word_timelines/ssl/distilr_news.key
COPY api_word_timelines/requirements.txt /usr/src/api_word_timelines/requirements.txt
RUN pip install -r /usr/src/api_word_timelines/requirements.txt

RUN mkdir /usr/src/api_word_timelines/api_word_timelines
COPY api_template/api_template/ /usr/src/api_word_timelines/api_word_timelines
COPY api_word_timelines/ /usr/src/api_word_timelines
