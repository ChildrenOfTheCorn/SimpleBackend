-- tables

-- Table: user
CREATE TABLE users (
    id int NOT NULL AUTO_INCREMENT,
    ean varchar(255) NOT NULL,
    name varchar(255) NOT NULL UNIQUE,
    password varchar(64) NOT NULL,
    token varchar(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (id)
) COMMENT 'Список пользователей';

-- Table: wallet_list
CREATE TABLE wallets (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE,
    currency varchar(10) NOT NULL,
    user_id int NOT NULL,
    CONSTRAINT wallets_pk PRIMARY KEY (id)
) COMMENT 'Список покупок';


-- Table: entry
CREATE TABLE entry (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    wallet_id int NOT NULL,
    user_id int NOT NULL,
    price int NOT NULL,
    CONSTRAINT entry_pk PRIMARY KEY (id)
) COMMENT 'Элементы списка';

-- Table: categories
CREATE TABLE categories (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE,
    CONSTRAINT category_pk PRIMARY KEY (id)
) COMMENT 'категории';

-- Table: services
CREATE TABLE services (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE,
    category_id int NOT NULL,
    CONSTRAINT category_pk PRIMARY KEY (id)
) COMMENT 'категории';

-- foreign keys
-- Reference: entry_shop_list (table: entry)
ALTER TABLE entry ADD CONSTRAINT entry_wallet FOREIGN KEY entry_wallet (wallet_id)
    REFERENCES wallets (id);

-- Reference: entry_user (table: entry)
ALTER TABLE entry ADD CONSTRAINT entry_user FOREIGN KEY entry_user (user_id)
    REFERENCES users (id);

-- Reference: wallet_users (table: wallets)
ALTER TABLE wallets ADD CONSTRAINT wallet_users FOREIGN KEY wallet_users (user_id)
    REFERENCES users (id);

ALTER TABLE `wallets` ADD UNIQUE `wallets_idx`(`user_id`, `currency`);



-- Reference: shop_list_users (table: shop_list)
ALTER TABLE services ADD CONSTRAINT service_category FOREIGN KEY service_category (category_id)
    REFERENCES categories (id);

-- End of file.

