CREATE DATABASE IF NOT EXISTS finguard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE finguard;
CREATE TABLE IF NOT EXISTS banks (id VARCHAR(16) PRIMARY KEY, name VARCHAR(160) NOT NULL);
CREATE TABLE IF NOT EXISTS financial_records (
 bank_id VARCHAR(16) NOT NULL, year SMALLINT NOT NULL,
 gross_open DOUBLE, gross_close DOUBLE, net_open DOUBLE, net_close DOUBLE, advances DOUBLE,
 tier1 DOUBLE, tier2 DOUBLE, car DOUBLE, interest_earned DOUBLE, interest_expended DOUBLE,
 nii DOUBLE, other_income DOUBLE, operating_expenses DOUBLE, net_profit DOUBLE,
 assets DOUBLE, previous_assets DOUBLE, borrowings DOUBLE, capital DOUBLE,
 reserves DOUBLE, deposits DOUBLE, lcr DOUBLE NULL,
 PRIMARY KEY (bank_id, year), FOREIGN KEY (bank_id) REFERENCES banks(id)
);
