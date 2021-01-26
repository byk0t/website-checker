CREATE TABLE IF NOT EXISTS website_check (
  url varchar(200) NOT NULL,
  http_code integer NOT NULL,
  response_time float NOT NULL,
  content_check bool NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);