create table pkk_cadastral_okrugs (
    id serial primary key, 
    id_type integer, 
    sort bigint, 
    attrs_cn varchar(30), 
    attrs_id varchar(30), 
    attrs_name varchar(50),
    center_x double precision, 
    center_y double precision, 
    extent_ymin double precision, 
    extent_ymax double precision, 
    extent_xmin double precision, 
    extent_xmax double precision,
    stat_rayon_total integer,
    stat_rayon_geo  integer,

    stat_kvartal_total integer,
    stat_kvartal_geo integer,

    stat_parcel_total integer,
    stat_parcel_geo integer,

    stat_oks_total integer,
    stat_oks_geo integer
);

CREATE INDEX pkk_cadastral_okrugs_index_cn ON public.pkk_cadastral_okrugs USING btree (attrs_cn);
CREATE INDEX pkk_cadastral_okrugs_index_id ON public.pkk_cadastral_okrugs USING btree (attrs_id);

create table pkk_cadastral_rayons (
    id serial primary key, 
    id_type integer, 
    sort bigint, 
    attrs_cn varchar(30), 
    attrs_id varchar(30), 
    attrs_name varchar(50),
    center_x double precision, 
    center_y double precision, 
    extent_ymin double precision, 
    extent_ymax double precision, 
    extent_xmin double precision, 
    extent_xmax double precision,

    stat_kvartal_total integer,
    stat_kvartal_geo integer,

    stat_parcel_total integer,
    stat_parcel_geo integer,

    stat_oks_total integer,
    stat_oks_geo integer
);

CREATE INDEX pkk_cadastral_rayons_index_cn ON public.pkk_cadastral_rayons USING btree (attrs_cn);
CREATE INDEX pkk_cadastral_rayons_index_id ON public.pkk_cadastral_rayons USING btree (attrs_id);

create table pkk_cadastral_kvartals (
    id serial primary key, 
    id_type integer, 
    sort bigint, 
    center_x double precision, 
    center_y double precision, 
    extent_ymin double precision, 
    extent_ymax double precision, 
    extent_xmin double precision, 
    extent_xmax double precision,

    stat_parcel_total integer,
    stat_parcel_geo integer,

    stat_oks_total integer,
    stat_oks_geo integer,
    
    attrs_cn varchar(30), 
    attrs_id varchar(30), 

    attrs_info text,

    attrs_cad_eng_organ varchar(500),

    attrs_customer_phone varchar(300),
    attrs_cad_eng_doc_date varchar(300),
    attrs_customer_email varchar(300),
    attrs_address varchar(300),
    attrs_status_id varchar(300),
    attrs_customer_address varchar(300),
    attrs_status varchar(300),
    attrs_date_begin varchar(300),
    attrs_rayon_cn varchar(300),
    attrs_contract_num varchar(300),
    attrs_contract_date varchar(300),
    attrs_date_end varchar(300),
    attrs_cad_eng_email varchar(300),
    attrs_cad_eng_phone varchar(300),
    attrs_customer_name varchar(300),
    attrs_contractor varchar(300),
    attrs_kkr varchar(300),
    attrs_cad_eng_doc_num varchar(300),
    attrs_cad_eng_name varchar(300),
    attrs_rayon varchar(300),
    attrs_cad_eng_address varchar(300)
);

CREATE INDEX pkk_cadastral_kvartals_index_cn ON public.pkk_cadastral_kvartals USING btree (attrs_cn);
CREATE INDEX pkk_cadastral_kvartals_index_id ON public.pkk_cadastral_kvartals USING btree (attrs_id);