LOAD DATA INFILE './travel_special.csv' INTO TABLE departments FIELDS TERMINATED BY ','IGNORE 1 LINES  (`name`, `code`);

LOAD DATA INFILE './region.csv' INTO TABLE regions FIELDS TERMINATED BY ',' IGNORE 1 LINES ( `region`  );

LOAD DATA INFILE './sector.csv' INTO TABLE sectors FIELDS TERMINATED BY ',' IGNORE 1 LINES ( `sector`  );


LOAD DATA INFILE './corona.csv' INTO TABLE patient FIELDS TERMINATED BY ',' IGNORE 1 LINES ( `region`, `2020-1`  ,`2020-2`  ,`2020-3`  ,`2020-4`  ,`2021-1`  ,`2021-2`  ,`2021-3` ,`2021-4`  );

LOAD DATA INFILE './result.csv' INTO TABLE sales FIELDS TERMINATED BY ',' IGNORE 1 LINES ( `sector` ,`qua_rev` ,`qua_sale`  ,`mon_sale` ,`tue_sale` ,
`wen_sale` ,`thur_sale` ,`fri_sale` ,`sat_sale` ,`sun_sale` ,`store` ,`region`,`year_mon`  );
