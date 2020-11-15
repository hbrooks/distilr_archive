# Goal:
To tell the story of an entity by measuring word use over time and in the context of the modeled entity. 

# Design:
The backend of the application is broken up into 2 parts: a pipeline to react to emerging news articles and a REST API to support the front end in visualization of the product.  A production grade system would be fun to build to time consuming and expensive as a lone developer.

## Pipeline Flow:
This pipeline needs to facilitate both live and historical collection of information into Distilr.  It should update the timelines when relevent articles are discovered, even when those articles came out a while ago.  

### Historical Ingestion:
Special web crawlers will scout news web sites and pass URLs into the pipeline.  This assumes RSS can't do historical content detection.  

### Live Ingestion:
A RSS Listener will subscribe to feeds of popular news networks.  When the listener becomes aware that a new article is available, it will pass the URL into the pipeline.

### Flow:
A REST API will provide the interface for this pipeline.  When a response is recieved by the pipeline:
1.  an entry in `content` is created
1.  pass the URL along to the crawler

The Crawler will:
1.  extract the text from the news article using Goose
1.  extract the `content.pub_date`
1.  store the raw text in a S3 bucket and update the `raw_text_url`
1.  notify the NLP processor

The NLP Processor will:
1.  expand conjugations
1.  filter out stop words 
1.  filter out non-nouns
1.  store the remaining words in S3 and update the `postprocessed_url`
1.  **Future**: create N grams from the remaining words
1.  store the n_grams as a JSON in S3 and update the `n_grams_url`
1.  notify the classifier

The Classifier will:
1.  **Future**: This step may be skipped while there is only a few timelines in development
1.  classify the content using simple RegExs for now and later a NN
1.  notify the builder

The Builder will:
1.  For each tag that the article is tagged with:
1.  rebuild the timeline by:
    1.  removing early outliers by dropping the first 0.5% of the data
    1.  creating 300 buckets of equal duration over the remaining time difference
    1.  picking the most popular 500 words
    1.  write each word to `tokens`
    1.  **Future**: get the n_grams that contain that word.
    1.  finding the average, normalized frequency of use for that time window
    1.  smooth the time windows using a SavGol filter
1.  store the frequency of use vector in a S3 bucket and update the `smoothed_frequency_url`
1.  store the frequency of use vector in a S3 bucket and update the `frequency_url`
1.  notify the popularity picker

The Popularity Picker will:
1.  for each of the 500 most popular words
1.  for each start time
1.  for each end time
1.  integrate the smoothed function over time
1.  store score in `top_words_index`



# DataBase Schema:

1.  sources:
    1.  id
    1.  RSS_id / name
    
1.  content:
    1.  source.id
    1.  url
    1.  pub_date
    1.  raw_text_url
    1.  postprocessed_url
    1.  n_grams_url
    1.  smoothed_frequency_url
    1.  frequency_url

1.  tags:
    1.  id
    1.  name

1.  classification:
    1.  id
    1.  content.id
    1.  tags.id

1.  tokens
    1.  id
    1.  value

1.  top_words_index
    1.  window_start
    1.  window_end
    1.  tag.id
    1.  token.id
    1.  popularity_score
    1.  **Future**: Reference an article that relates to this token from this time period here.



## Service Flow:
With the above approach, the frontend only needs to supply:
1.  window_start
1.  window_end
1.  tag.id
in order to quickly get the most popular tokens for a time range.  In order to get the trend over time for that token, all the backend needs to do is filter `smoothed` by token and by time.  The time filtering can be done by using a binary search.

The service is simply a REST API over the database.