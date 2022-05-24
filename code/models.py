from peewee import PostgresqlDatabase, Model, PrimaryKeyField, IntegerField, TextField, DoubleField, CharField
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST
database = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    autorollback=True
)
class BaseModel(Model):
    class Meta:
        database = database

class CadastralOkrug(BaseModel):
    id = PrimaryKeyField(null=False)
    id_type = IntegerField(null=True)
    sort = IntegerField(null=True)

    attrs_name = CharField(null=True)
    attrs_cn = CharField(null=True)
    attrs_id = CharField(null=True)

    center_x = DoubleField(null=True)
    center_y = DoubleField(null=True)
    
    extent_ymin = DoubleField(null=True)
    extent_ymax = DoubleField(null=True)
    extent_xmin = DoubleField(null=True)
    extent_xmax = DoubleField(null=True)

    stat_rayon_total = IntegerField(null=True)
    stat_rayon_geo = IntegerField(null=True)

    stat_kvartal_total = IntegerField(null=True)
    stat_kvartal_geo = IntegerField(null=True)

    stat_parcel_total = IntegerField(null=True)
    stat_parcel_geo = IntegerField(null=True)

    stat_oks_total = IntegerField(null=True)
    stat_oks_geo = IntegerField(null=True)

    class Meta:
        table_name = 'pkk_cadastral_okrugs'
class CadastralRayon(BaseModel):
    id = PrimaryKeyField(null=False)
    id_type = IntegerField(null=True)
    sort = IntegerField(null=True)

    attrs_name = CharField(null=True)
    attrs_cn = CharField(null=True)
    attrs_id = CharField(null=True)

    center_x = DoubleField(null=True)
    center_y = DoubleField(null=True)
    
    extent_ymin = DoubleField(null=True)
    extent_ymax = DoubleField(null=True)
    extent_xmin = DoubleField(null=True)
    extent_xmax = DoubleField(null=True)

    stat_kvartal_total = IntegerField(null=True)
    stat_kvartal_geo = IntegerField(null=True)

    stat_parcel_total = IntegerField(null=True)
    stat_parcel_geo = IntegerField(null=True)

    stat_oks_total = IntegerField(null=True)
    stat_oks_geo = IntegerField(null=True)

    class Meta:
        table_name = 'pkk_cadastral_rayons'

class CadastralKvartal(BaseModel):
    id = PrimaryKeyField(null=False)
    id_type = IntegerField(null=True)
    sort = IntegerField(null=True)

    attrs_cn = CharField(null=True)
    attrs_id = CharField(null=True)

    center_x = DoubleField(null=True)
    center_y = DoubleField(null=True)
    
    extent_ymin = DoubleField(null=True)
    extent_ymax = DoubleField(null=True)
    extent_xmin = DoubleField(null=True)
    extent_xmax = DoubleField(null=True)

    attrs_info = TextField(null=True)

    attrs_customer_phone = CharField(null=True)
    attrs_cad_eng_doc_date = CharField(null=True)
    attrs_customer_email = CharField(null=True)
    attrs_address = CharField(null=True)
    attrs_status_id = CharField(null=True)
    attrs_customer_address = CharField(null=True)
    attrs_status = CharField(null=True)
    attrs_date_begin = CharField(null=True)
    attrs_rayon_cn = CharField(null=True)
    attrs_contract_num = CharField(null=True)
    attrs_contract_date = CharField(null=True)
    attrs_date_end = CharField(null=True)
    attrs_cad_eng_email = CharField(null=True)
    attrs_cad_eng_phone = CharField(null=True)
    attrs_customer_name = CharField(null=True)
    attrs_contractor = CharField(null=True)
    attrs_kkr = CharField(null=True)
    attrs_cad_eng_doc_num = CharField(null=True)
    attrs_cad_eng_organ = CharField(null=True)
    attrs_cad_eng_name = CharField(null=True)
    attrs_rayon = CharField(null=True)
    attrs_cad_eng_address = CharField(null=True)

    class Meta:
        table_name = 'pkk_cadastral_kvartals'