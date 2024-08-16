USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.mathfactdata (
  number TEXT,
  text TEXT,
  PRIMARY KEY (number,text)
);