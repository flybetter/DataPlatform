drop table if exists phone_profile_log;
create table phone_profile_log (
  ID          bigint(20)   not null auto_increment
  comment 'id',
  PHONE       int(11)      not null
  comment 'phone number',
  CITY        varchar(200) not null
  comment 'city',
  SOURCE      int(11)      not null
  comment ' 1:crm ,2 the whole chain',
  SOURCE_ID   bigint(20)            default null
  comment 'the id from source',
  BEDROOM     float(5, 2)           default null
  comment 'bedroom',
  AVG_PRICE   float(8, 2)           default null
  comment 'avg_price',
  SUM_PRICE   float(5, 2)           default null
  comment 'sum_price',
  KITCHEN     float(5, 2)           default null
  comment 'kitchen',
  TOLIET      float(5, 2)           default null
  comment 'toliet',
  LIVINGROOM  float(5, 2)           default null
  comment 'livingroom',
  AREA        float(8, 2)           default null
  comment 'area',
  CREATE_TIME timestamp    NULL     default CURRENT_TIMESTAMP
  COMMENT 'create time',
  primary key (id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;




