﻿-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2016-07-31 16:12:33.561

-- foreign keys
ALTER TABLE entry DROP FOREIGN KEY entry_wallet;
ALTER TABLE entry DROP FOREIGN KEY entry_user;
ALTER TABLE entry DROP FOREIGN KEY entry_service;

ALTER TABLE wallets DROP FOREIGN KEY wallet_users;

ALTER TABLE services DROP FOREIGN KEY service_category;

ALTER TABLE confirmations DROP FOREIGN KEY confirmations_users;
ALTER TABLE confirmations DROP FOREIGN KEY confirmations_services;
ALTER TABLE confirmations DROP FOREIGN KEY confirmations_wallets;

-- tables
DROP TABLE entry;

DROP TABLE wallets;

DROP TABLE services;

DROP TABLE categories;

DROP TABLE users;

DROP TABLE confirmations;

-- End of file.

