# Dialect Translation Reference

> Reference file for the `query-language-coach` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

### 2. Dialect Translation Reference
| Task | SQL Server (T-SQL) | Oracle | PostgreSQL | MySQL |
| :--- | :--- | :--- | :--- | :--- |
| First N rows | `SELECT TOP (10) …` or `OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY` (needs `ORDER BY`) | `FETCH FIRST 10 ROWS ONLY` (12c+); `ROWNUM` in legacy code | `LIMIT 10` or `FETCH FIRST 10 ROWS ONLY` | `LIMIT 10` |
| Paging | `ORDER BY … OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` | `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` | `LIMIT 10 OFFSET 20` | `LIMIT 20, 10` or `LIMIT 10 OFFSET 20` |
| Join strings | `CONCAT(a, b)` or `a + b` (NULL makes `+` return NULL) | `a \|\| b` (NULLs act as empty) | `a \|\| b` (NULL makes it NULL); `concat()` skips NULLs | `CONCAT(a, b)` (`\|\|` means OR by default) |
| Replace NULL | `ISNULL(x, 0)` or `COALESCE` | `NVL(x, 0)` or `COALESCE` | `COALESCE(x, 0)` | `IFNULL(x, 0)` or `COALESCE` |
| Current date/time | `SYSDATETIME()`, `GETDATE()` | `SYSDATE`, `SYSTIMESTAMP` | `now()`, `CURRENT_TIMESTAMP` | `NOW()` |
| Add 7 days | `DATEADD(day, 7, d)` | `d + 7` or `d + INTERVAL '7' DAY` | `d + INTERVAL '7 days'` | `DATE_ADD(d, INTERVAL 7 DAY)` |
| Auto-number key | `INT IDENTITY(1,1)` | `GENERATED ALWAYS AS IDENTITY` (12c+) or a sequence | `GENERATED ALWAYS AS IDENTITY` (preferred over `SERIAL`) | `AUTO_INCREMENT` |
| Insert-or-update (upsert) | `MERGE` (test concurrency carefully) | `MERGE` | `INSERT … ON CONFLICT … DO UPDATE`; `MERGE` (15+) | `INSERT … ON DUPLICATE KEY UPDATE` |
| Combine values into a list | `STRING_AGG(col, ', ')` (2017+) | `LISTAGG(col, ', ') WITHIN GROUP (ORDER BY col)` | `string_agg(col, ', ')` | `GROUP_CONCAT(col SEPARATOR ', ')` |
| True/false type | `BIT` (0/1) | `BOOLEAN` (23ai/26ai); `NUMBER(1)` or `CHAR(1)` in older versions | `BOOLEAN` | `BOOLEAN` (alias for `TINYINT(1)`) |
| Quote an identifier | `[Order Date]` or `"Order Date"` | `"Order Date"` (case-sensitive once quoted) | `"Order Date"` | `` `Order Date` `` |
| Temporary table | `#temp` (session), `##temp` (global) | Global or private temporary table (18c+) | `CREATE TEMP TABLE` | `CREATE TEMPORARY TABLE` |
| Show the plan | Actual execution plan in SSMS; `SET STATISTICS IO, TIME ON` | `EXPLAIN PLAN FOR …` + `DBMS_XPLAN.DISPLAY`; `DBMS_XPLAN.DISPLAY_CURSOR` | `EXPLAIN (ANALYZE, BUFFERS) …` | `EXPLAIN ANALYZE …`, `EXPLAIN FORMAT=TREE` |
| JSON field | `JSON_VALUE(doc, '$.city')`; native `json` type (2025) | `JSON_VALUE(doc, '$.city')` or dot notation on JSON columns | `doc->>'city'` (`jsonb`) | `doc->>'$.city'` |
| Procedural language | T-SQL batches and stored procedures | PL/SQL | PL/pgSQL (plus other languages) | Stored programs (`BEGIN … END`, `DELIMITER` in the client) |

**Behavior differences to always check when translating:**
- **Empty string vs. NULL:** Oracle treats `''` as NULL; the others don't.
- **Case sensitivity:** SQL Server and MySQL default collations are usually case-insensitive; PostgreSQL and Oracle compare case-sensitively by default. PostgreSQL folds unquoted identifiers to lowercase; Oracle folds them to uppercase.
- **Integer division:** `5/2` returns `2` in SQL Server and PostgreSQL but `2.5` in Oracle and MySQL. Cast to decimal when you want the fraction.
- **Dates:** SQL Server `DATETIME` rounds to about 3 ms (use `DATETIME2`); Oracle `DATE` includes a time portion.
- **`FROM DUAL`:** required in Oracle before 23ai/26ai for `SELECT` without a table; optional now.
- **Transactions:** Oracle doesn't auto-commit by default in many tools; SQL Server, PostgreSQL, and MySQL clients usually do. DDL auto-commits in Oracle and MySQL but is transactional in PostgreSQL and SQL Server.
