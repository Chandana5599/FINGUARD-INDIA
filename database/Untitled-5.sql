USE finguard;

SELECT COUNT(*) AS imported_rows
FROM rbi_import_staging;
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = ON;
SHOW GLOBAL VARIABLES LIKE 'local_infile';