
UPDATE
  bdms.config
SET
  value_cfg = '1.0.1'
WHERE
  name_cfg = 'VERSION';

UPDATE
  bdms.config
SET
  value_cfg = '1.0.0'
WHERE
  name_cfg = 'PREVIOUS';

UPDATE
  bdms.config
SET
  value_cfg = '1.0.0'
WHERE
  name_cfg = 'GEOLCODES';

UPDATE
  bdms.config
SET
  value_cfg = to_char(now(), 'YYYY-MM-DD"T"HH24:MI:SSOF'))
WHERE
  name_cfg = 'PG_UPGRADE';

CREATE TABLE bdms.files (
    id_fil serial,
    id_usr_fk integer,
    name_fil character varying NOT NULL,
    hash_fil character varying NOT NULL,
    type_fil character varying NOT NULL,
    uploaded_fil timestamp with time zone DEFAULT now(),
    conf_fil json,
    PRIMARY KEY (id_fil),
    CONSTRAINT files_id_usr_fkey FOREIGN KEY (id_usr_fk)
        REFERENCES bdms.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE bdms.borehole_files
(
    id_bho_fk integer NOT NULL,
    id_fil_fk integer NOT NULL,
    id_usr_fk integer,
    attached_bfi timestamp with time zone DEFAULT now(),
    update_bfi timestamp with time zone DEFAULT now(),
    updater_bfi integer,
    description_bfi character varying,
    public_bfi boolean DEFAULT true,
    PRIMARY KEY (id_bho_fk, id_fil_fk),
    CONSTRAINT borehole_files_id_usr_fkey FOREIGN KEY (id_usr_fk)
        REFERENCES bdms.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE bdms.terms
(
    id_tes serial NOT NULL,
    draft_tes boolean NOT NULL DEFAULT TRUE,
    text_tes_en character varying NOT NULL,
    text_tes_de character varying,
    text_tes_fr character varying,
    text_tes_it character varying,
    text_tes_ro character varying,
    creation_tes timestamp with time zone NOT NULL DEFAULT now(),
    expired_tes timestamp with time zone,
    PRIMARY KEY (id_tes)
);

CREATE TABLE bdms.terms_accepted (
    id_usr_fk integer NOT NULL,
    id_tes_fk integer NOT NULL,
    accepted_tea timestamp with time zone DEFAULT now(),
    PRIMARY KEY (id_usr_fk, id_tes_fk),
    FOREIGN KEY (id_usr_fk)
        REFERENCES bdms.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (id_tes_fk)
        REFERENCES bdms.terms (id_tes) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE bdms.feedbacks
(
    id_feb serial NOT NULL,
    created_feb timestamp with time zone DEFAULT now(),
    user_feb character varying NOT NULL,
    message_feb character varying,
    tag_feb character varying,
    frw_feb boolean DEFAULT false,
    PRIMARY KEY (id_feb)
);