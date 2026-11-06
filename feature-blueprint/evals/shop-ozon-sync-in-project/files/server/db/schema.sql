CREATE TABLE categories (id serial PRIMARY KEY, name text NOT NULL UNIQUE);
CREATE TABLE products (
  id serial PRIMARY KEY,
  sku text NOT NULL UNIQUE,
  name text NOT NULL,
  price_kopecks integer NOT NULL CHECK (price_kopecks >= 0),
  stock integer NOT NULL DEFAULT 0,
  category_id integer REFERENCES categories(id),
  updated_at timestamptz NOT NULL DEFAULT now()
);
