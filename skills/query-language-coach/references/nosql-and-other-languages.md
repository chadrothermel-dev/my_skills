# NoSQL, Graph & Other Query Languages

> Reference file for the `query-language-coach` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

### 4. NoSQL, Graph & Other Query Languages
| Language / API | Database | Plain-language idea | Example |
| :--- | :--- | :--- | :--- |
| MongoDB Query API (MQL) | MongoDB, Cosmos DB for MongoDB | Ask for documents that match a pattern | `db.customers.find({ state: "PA" }, { name: 1, email: 1 })` |
| Aggregation pipeline | MongoDB | An assembly line of steps: filter → group → sort | `db.orders.aggregate([{ $match: { status: "A" } }, { $group: { _id: "$customerId", total: { $sum: "$amount" } } }])` |
| CQL | Apache Cassandra, Amazon Keyspaces | SQL-like, but you must query by the partition key; no joins | `SELECT * FROM orders_by_customer WHERE customer_id = ?;` |
| Redis commands | Redis, Valkey | Store and fetch by exact key | `SET session:42 "…" EX 3600` · `GET session:42` |
| Key conditions / PartiQL | Amazon DynamoDB | `Query` uses the key (fast); `Scan` reads everything (slow, costly) | `SELECT * FROM Orders WHERE CustomerId = 'C42'` |
| NoSQL query language | Azure Cosmos DB for NoSQL | SQL-like queries over JSON; include the partition key to keep cost (RUs) low | `SELECT c.name FROM c WHERE c.state = "PA"` |
| Cypher / GQL | Neo4j and other graph databases (GQL is the ISO standard graph query language) | Draw the pattern of connected things you want | `MATCH (p:Person {name:'Ana'})-[:FRIEND]->(f) RETURN f.name` |
| Gremlin | Amazon Neptune, Cosmos DB for Apache Gremlin, other Apache TinkerPop databases | Walk the graph step by step | `g.V().has('name','Ana').out('friend').values('name')` |
| KQL | Azure Data Explorer and Microsoft Fabric Real-Time Intelligence | A pipeline: start with a table, then pipe through steps | `Requests \| where Status >= 500 \| summarize count() by bin(Timestamp, 1h)` |
| Vector search | pgvector, SQL Server 2025 / Azure SQL, Oracle AI Vector Search | "Find the rows most similar in meaning" | pgvector: `ORDER BY embedding <=> $1 LIMIT 5` · T-SQL: `VECTOR_DISTANCE('cosine', embedding, @q)` · Oracle: `VECTOR_DISTANCE(embedding, :q, COSINE)` |

When translating SQL to a NoSQL language, explain the modeling shift: NoSQL databases usually expect you to store data shaped the way it's read (embedding, duplicating, one table per query) instead of joining at query time.
