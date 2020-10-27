
UPDATE
  bdms.config
SET
  value_cfg = '1.0.2'
WHERE
  name_cfg = 'VERSION';

UPDATE
  bdms.config
SET
  value_cfg = '1.0.1'
WHERE
  name_cfg = 'PREVIOUS';

UPDATE
  bdms.config
SET
  value_cfg = to_char(now(), 'YYYY-MM-DD"T"HH24:MI:SSOF')
WHERE
  name_cfg = 'PG_UPGRADE';

CREATE TABLE bdms.contents (
    id_cnt serial,
    name_cnt character varying NOT NULL,
    draft_cnt boolean NOT NULL DEFAULT true,

    title_cnt_en character varying,
    text_cnt_en character varying,

    title_cnt_de character varying,
    text_cnt_de character varying,

    title_cnt_fr character varying,
    text_cnt_fr character varying,

    title_cnt_it character varying,
    text_cnt_it character varying,

    title_cnt_ro character varying,
    text_cnt_ro character varying,

    creation_cnt timestamp with time zone  DEFAULT now(),
    expired_cnt timestamp with time zone,

    PRIMARY KEY (id_cnt)
);


INSERT INTO bdms.contents(
	name_cnt,
	draft_cnt,
    
    title_cnt_en,
    text_cnt_en,
    
    title_cnt_de,
    text_cnt_de,
    
    title_cnt_fr,
    text_cnt_fr,
    
    title_cnt_it,
    text_cnt_it

) VALUES (
    'login',
    FALSE,
    
    'Welcome to swissforage.ch',
    'A platform to acquire borehole data according to the Borehole data model defined by the Swiss Geological Survey at swisstopo ([more](https://geoservice.ist.supsi.ch/docs/bdms)).',
    
    'Willkommen bei swissforage.ch',
    'Eine Plattform zur Erfassung von Bohrlochdaten nach dem von der Schweizerischen Landesgeologie bei swisstopo definierten Bohrlochdatenmodell ([mehr](https://geoservice.ist.supsi.ch/docs/bdms)).',
    
    'Bienvenue sur swissforage.ch',
    'Une plate-forme pour l''acquisition de données de forage selon le modèle de données de forage défini par le Service géologique suisse à swisstopo ([en savoir plus](https://geoservice.ist.supsi.ch/docs/bdms)).',
    
    'Benvenuti su swissforage.ch',
    'Una piattaforma per l''acquisizione di dati di trivellazione secondo il modello di dati di trivellazione definito dal Servizio geologico nazionale di swisstopo ([altro](https://geoservice.ist.supsi.ch/docs/bdms)).'
);