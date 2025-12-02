-- Create Database
CREATE DATABASE media ENCODING = 'UTF8';

-- Create User dragibus
CREATE USER media WITH ENCRYPTED PASSWORD 'media';

GRANT CONNECT ON DATABASE media TO media;
GRANT USAGE ON SCHEMA public TO media;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO media;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO media;

\connect music

--Creation
CREATE SCHEMA IF NOT EXISTS "media";

GRANT ALL PRIVILEGES ON SCHEMA "media" TO media;
GRANT USAGE ON SCHEMA "media" TO media;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "media" TO media;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA "media" TO media;

--set default schema
ALTER USER media SET search_path = "media";

SET search_path TO "media";

CREATE OR REPLACE LANGUAGE plpgsql;
