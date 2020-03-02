
/*Creacion de la Base de datos*/
DROP DATABASE IF EXISTS dbeum_tecamac;
CREATE DATABASE dbeum_tecamac WITH OWNER eumdb;

\c dbeum_tecamac;

/*Creacion de las tablas de la BD */
\i BDEum.sql

/*Insercion de datos en los catalogos*/
\i catalogos.sql

GRANT ALL ON DATABASE dbeum_tecamac to eumdb;
GRANT ALL ON ALL TABLES IN SCHEMA public TO eumdb;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO eumdb;

