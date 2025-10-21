---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-ttl",
  "h1": "langsmith-self-host-ttl",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.458205",
  "sha256_raw": "aeffb3125b32de44cefa2d1d092d438bae60bc47100617a1710bb6befd5d0215"
}
---

# langsmith-self-host-ttl

> Source: https://docs.langchain.com/langsmith/self-host-ttl

Requirements
You can configure retention through helm or environment variable settings. There are a few options that are configurable:- Enabled: Whether data retention is enabled or disabled. If enabled, via the UI you can your default organization and project TTL tiers to apply to traces (see data retention guide for details).
- Retention Periods: You can configure system-wide retention periods for shortlived and longlived traces. Once configured, you can manage the retention level at each project as well as set an organization-wide default for new projects.
ClickHouse TTL Cleanup Job
As of version 0.11, a cron job runs on weekends to assist in deleting expired data that may not have been cleaned up by ClickHouse’s built-in TTL mechanism.This job uses potentially long running mutations (
ALTER TABLE DELETE
), which are expensive operations that can impact ClickHouse’s performance. We recommend running these operations only during off-peak hours (nights and weekends). During testing with 1 concurrent active mutation (default), we did not observe significant CPU, memory, or latency increases.Default Schedule
By default, the cleanup job runs:- Saturday: 8pm and 10pm UTC
- Sunday: 12am, 2am, and 4am UTC
Disabling the Job
To disable the cleanup job entirely:Configuring the Schedule
You can customize when the cleanup job runs by modifying the cron expressions:To run the job on a single cron schedule, set both
CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_EVENING
and CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_MORNING
to the same value. Job locking prevents overlapping executions.Configuring Minimum Expired Rows Per Part
The job goes table by table, scanning parts and deleting data from parts containing a minimum number of expired rows. This threshold balances efficiency and thoroughness:- Too low: Job scans entire parts to clear minimal data (inefficient)
- Too high: Job misses parts with significant expired data
Checking Expired Rows
Use this query to analyze expired rows in your tables, and tweak your minimum value accordingly:Configuring Maximum Active Mutations
Delete operations can be time-consuming (~50 minutes for a 100GB part). You can increase concurrent mutations to speed up the process:Increasing concurrent DELETE operations can severely impact system performance. Monitor your system carefully and only increase this value if you can tolerate potentially slower insert and read latencies.
Emergency: Stopping Running Mutations
If you experience latency spikes and need to terminate a running mutation:-
Find active mutations:
Look for the
mutation_id
where thecommand
column contains aDELETE
statement. -
Kill the mutation:
Backups and Data Retention
If disk space does not decrease after running this job, or if it continues to increase, backups may be causing the issue by creating file system hard links. These links prevent ClickHouse from cleaning up the data. To verify, check the following directories inside your ClickHouse pod:/var/lib/clickhouse/backup
/var/lib/clickhouse/shadow