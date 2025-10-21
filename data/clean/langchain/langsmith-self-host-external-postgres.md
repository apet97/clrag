---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-external-postgres",
  "h1": "langsmith-self-host-external-postgres",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.449601",
  "sha256_raw": "880e5305cdc115da7adb1d50eaf77c7ea1d7536b163505424a73ec2ac4a689e8"
}
---

# langsmith-self-host-external-postgres

> Source: https://docs.langchain.com/langsmith/self-host-external-postgres

LangSmith uses a PostgreSQL database as the primary data store for transactional workloads and operational data (almost everything besides runs). By default, LangSmith Self-Hosted will use an internal PostgreSQL database. However, you can configure LangSmith to use an external PostgreSQL database (). By configuring an external PostgreSQL database, you can more easily manage backups, scaling, and other operational tasks for your database.
Note: We only officially support PostgreSQL versions >= 14.
A user with admin access to the PostgreSQL database. This user will be used to create the necessary tables, indexes, and schemas.
This user will also need to have the ability to create extensions in the database. We use/will try to install the btree_gin, btree_gist, pgcrypto, citext, and pg_trgm extensions.
If using a schema other than public, ensure that you do not have any other schemas with the extensions enabled, or you must include that in your search path.
Support for pgbouncer and other connection poolers is community-based. Community members have reported that pgbouncer has worked with pool_mode = session and a suitable setting for ignore_startup_parameters (as of writing, search_path and lock_timeout need to be ignored). Care is needed to avoid polluting connection pools; some level of PostgreSQL expertise is advisable. LangChain Inc currently does not have roadmap plans for formal test coverage or commercial support of pgbouncer or amazon rds proxy or any other poolers, but the community is welcome to discuss and collaborate on support through GitHub issues.
By default, we recommend an instance with at least 2 vCPUs and 8GB of memory. However, the actual requirements will depend on your workload and the number of users you have. We recommend monitoring your PostgreSQL instance and scaling up as needed.
With your connection string in hand, you can configure your LangSmith instance to use an external PostgreSQL database. You can do this by modifying the values file for your LangSmith Helm Chart installation or the .env file for your Docker installation.
Once configured, you should be able to reinstall your LangSmith instance. If everything is configured correctly, your LangSmith instance should now be using your external PostgreSQL database.