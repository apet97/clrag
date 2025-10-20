# troubleshooting-project-status-match

> Source: https://clockify.me/help/troubleshooting/project-status-match

Project status and reports don’t match
If you’re seeing different numbers between the Project status page and the Detailed or Summary reports, here’s a breakdown of why the values may not match and how to interpret them correctly.
Project status shows all-time totals #
The Project status page always shows data from the start of the project to the current date. It does not respond to any date range filters.
What this means:
- If you run a report for last month, but the project started earlier, you’ll see a lower total in the report.
- The project status will show the full total from day one of the project.
How to match them more closely:
- Extend the report date range to cover the full project duration if you want to compare values.
Time rounding doesn’t apply to project status #
Time rounding rules set in Workspace settings only affect reports and exports, not the project status page.
What this means:
- If you’ve rounded time entries (e.g., to the nearest 6 minutes), reports will reflect that rounded value
- The project status page will use actual tracked time (unrounded), resulting in small differences
How to check:
- Open the Detailed report and turn off the rounding
- You’ll likely see values that more closely match the project status
Invoiced time is not deducted from the project status #
Invoicing a time entry does not remove or subtract it from the project’s tracked time or progress.
What this means:
- If you’ve already invoiced 20 hours, you might expect those to be removed from the project
- They’ll still be counted in full as project status tracks total effort, not outstanding or un-invoiced time
Project status is always displayed in decimal format #
Regardless of how your workspace is configured (e.g., full, compact, or decimal format), the Project status page will always show time in decimal format.
What this means:
- If your report says 1h 30m, the Project status page will display that as 1.5h
- This is just a difference in formatting, not an error or miscalculation
Use the Detailed report in the decimal format if you want a side-by-side comparison that matches the project status format.
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and include the following details:
- A screenshot of the Project status page for the project in question
- A screenshot of the report you’re comparing it to