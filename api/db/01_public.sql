DROP TABLE IF EXISTS account CASCADE;
CREATE TABLE account
(
  id bigserial NOT NULL,
  name text,
  password text,
  mail text,
  phone text,
  role int,
  search_str text,
  order_num bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_item PRIMARY KEY (id)
);
