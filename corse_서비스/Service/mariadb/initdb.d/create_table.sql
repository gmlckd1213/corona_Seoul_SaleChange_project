CREATE TABLE departments (
    `name`      VARCHAR(255)  NOT NULL ,
    `code`  VARCHAR(255)      NOT NULL UNIQUE,
    PRIMARY KEY (code)
);


CREATE TABLE regions (
    `region` VARCHAR(255)    NOT NULL,
    PRIMARY KEY (region)
);

CREATE TABLE patient (
    `region`  VARCHAR(255)   NOT NULL ,
    `2020-1`  INT   NOT NULL ,
    `2020-2`  INT   NOT NULL,
    `2020-3`  INT   NOT NULL,
    `2020-4`  INT   NOT NULL,
    `2021-1`  INT   NOT NULL,
    `2021-2`  INT   NOT NULL,
    `2021-3`  INT   NOT NULL,
    `2021-4`  INT   NOT NULL,
    PRIMARY KEY (region),
    FOREIGN KEY (region) REFERENCES regions(region)

);


CREATE TABLE sectors (
    `sector` VARCHAR(255)    NOT NULL,
    PRIMARY KEY (sector)
);



CREATE TABLE sales (
    `id` INT(64)    NOT NULL AUTO_INCREMENT, 
    `sector` VARCHAR(255)    NOT NULL,
    `qua_rev` BIGINT NOT NULL,
    `qua_sale` INT(64) NOT NULL,
    `mon_sale` BIGINT NOT NULL,
    `tue_sale` BIGINT NOT NULL,
    `wen_sale` BIGINT NOT NULL,
    `thur_sale` BIGINT NOT NULL,
    `fri_sale` BIGINT NOT NULL,
    `sat_sale` BIGINT NOT NULL,
    `sun_sale` BIGINT NOT NULL,
    `store` INT(64) NOT NULL,
    `region` VARCHAR(255)    NOT NULL,
    `year_mon` VARCHAR(255) NOT NULL ,

    PRIMARY KEY(id),
    FOREIGN KEY(sector) REFERENCES  sectors(sector),
    FOREIGN KEY (region) REFERENCES regions(region)
);

