CREATE TABLE IF NOT EXISTS documents (
    id CHAR(56) PRIMARY KEY UNIQUE, -- url_hash
    url TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS processed_documents (
    id CHAR(36) PRIMARY KEY UNIQUE, -- UUID
    documents_id CHAR(56) NOT NULL,
    processed_at DATETIME NOT NULL,
    processing_engine_verion TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published_at DATETIME NOT NULL,
    processed_words TEXT NOT NULL,
    ordered_tokens TEXT NOT NULL,
    counted_tokens TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS content_categories (
    id CHAR(36) PRIMARY KEY UNIQUE,
    name TEXT NOT NULL); 

CREATE TABLE IF NOT EXISTS tagging (
    id CHAR(36) PRIMARY KEY UNIQUE,
    tagging_method TEXT NOT NULL,
    tagging_engine_version TEXT NOT NULL,
    documents_id CHAR(56) NOT NULL,
    content_categories_id CHAR(36) NOT NULL,
    score TEXT NOT NULL);


CREATE TABLE IF NOT EXISTS timelines (
    id CHAR(36) PRIMARY KEY UNIQUE,
    content_categories_id CHAR(36) NOT NULL,
    document_hash TEXT NOT NULL,
    timeline_engine_verion TEXT NOT NULL,
    pickle_file_location TEXT NOT NULL);


CREATE TABLE IF NOT EXISTS timeline_query_results (
    timeline_id CHAR(36) NOT NULL,
    -- TODO: Add start/end date.
    data TEXT NOT NULL);
