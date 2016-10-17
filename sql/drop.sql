﻿-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2016-07-31 16:12:33.561

-- foreign keys
ALTER TABLE entry
    DROP FOREIGN KEY entry_wallet;

ALTER TABLE wallets
    DROP FOREIGN KEY wallet_users;

ALTER TABLE users
    DROP FOREIGN KEY user_entries;

ALTER TABLE services
    DROP FOREIGN KEY service_category;

-- tables
DROP TABLE entry;

DROP TABLE wallets;

DROP TABLE services;

DROP TABLE categories;

DROP TABLE users;

-- End of file.

