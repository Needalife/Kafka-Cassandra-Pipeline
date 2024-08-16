USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  name TEXT,
  address TEXT,
  year INT,
  country TEXT,
  company TEXT,
  job TEXT,
  prefix TEXT,
  color_name TEXT,
  ascii_email TEXT,
  phone_number TEXT,
  PRIMARY KEY (name, address)
);