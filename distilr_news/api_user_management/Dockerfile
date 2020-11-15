FROM python:3.7

WORKDIR /usr/src/api_user_management

# Copy this before the source code to take advantage of cacheing container layers.
RUN mkdir /usr/src/api_user_management/ssl
# COPY shared/ssl/distilr_news.csr /usr/src/api_user_management/ssl/distilr_news.csr
# COPY shared/ssl/distilr_news.key /usr/src/api_user_management/ssl/distilr_news.key
COPY api_user_management/requirements.txt /usr/src/api_user_management/requirements.txt
RUN pip install -r /usr/src/api_user_management/requirements.txt

RUN mkdir /usr/src/api_user_management/api_user_management
COPY api_template/api_template/ /usr/src/api_user_management/api_user_management
COPY api_user_management/ /usr/src/api_user_management
