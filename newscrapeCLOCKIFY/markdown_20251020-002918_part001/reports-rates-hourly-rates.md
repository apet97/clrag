# reports-rates-hourly-rates

> Source: https://clockify.me/help/reports/rates/hourly-rates

Overview of hourly rates
Clockify can apply different hourly rates to your billable time entries and show how much money you earn in reports.
Clockify multiplies each billable time entry with their corresponding hourly rate and that number is shown as earning in a report.
In order for Clockify to calculate hourly rates, you first have to mark time entries as billable in the Time Tracker (or in the Detailed report) by clicking on the $ sign.
If you don’t use hourly rates, you can completely remove all the billable information from interface for everyone by turning off Activate billable hours in Workspace Settings > Permissions tab, or you can hide it just for regular users.
Hourly rate types #
There are several types of hourly rates in Clockify:
- Workspace rate, which you define in Workspace settings; it gets applied to all billable time rates unless it gets overridden by a more specific billable rate
- Member rate, which you define on Team page for each user
- Project rate, which you define for each project
- Task rate, if enabled in workspace settings
- Projects’ member rate, which you define in projects’ Access tab
In addition to billable rates, you can also have one more set of rates for labor cost.
Hourly rate hierarchy #
Project’s member rate > Task rate > Project rate > Member rate > Workspace rate
Applied billable rate #
A more specific billable rate overrides a less specific one:
Project’s member rate > Task rate > Project rate > Member rate > Workspace rate.
For example, let’s say you’re a freelancer and you have a default rate you charge on all projects. You define that rate as your workspace billable rate. Then, you also have a client to whom you charge a different rate. In that case, you can create a project, assign it to the client, and set the desired hourly rate for that project.
To set different pricing per client at project level:
- Create different projects
- Assign them to respective clients
- Go to Projects and click the project name
- Click Settings tab
- Set the desired billable rate for each project in Project billable rate section
You can’t assign a custom billable rate for a specific time entry. But, you can use a tag to indicate a special billable rate so you know how much to charge when preparing an invoice.
Set custom currency #
To change currency, click on Settings in the left sidebar then when in the Workspace settings type your currency instead of USD. You can add multiple currencies on a workspace, or assign different currencies to multiple clients.
Currency can only be edited by the workspace administrator and it’s applied to the whole account (including billable rates).
Who can set hourly rates #
Only workspace admin can set hourly rates for workspace, user, and project.
Project managers can set hourly rates for people on their projects if Who can see billable rates in workspace settings is set to everyone.
Regular members can’t set or edit any hourly rates.
For more info, check out the Understanding user roles & access permissions article.
Share additional data with employees #
If you wish your employees to see their earnings and hourly rates, but don’t wish them to see other people’s rates or want to limit them to seeing just cost rates, you can create a shared report:
- Open Summary or Detailed report
- Filter by employee
- Choose if you wish to display amount, cost, or profit
- Click on share icon
- Name the report and set it to private
- Choose who can view the report
- Your employee can now access the report you’ve created
Project and task billability #
You can change whether time entries on a project are billable or non-billable by default.
You can set project’s default billability status when you click on a project from the Projects page and go to the Project Settings tab.
If you set the project as billable, when someone tracks time and doesn’t specify billability, the time entry will be marked as billable (which you can edit later).
It’s possible to change the billable status the same way you set it, in the Project Settings tab. Once the project’s billable status is changed e.g. from billable to non-billable this will not affect previously created time entries. Their status will remain the same as it was when it was created. However, all new time entries linked to that project will automatically be set to the new status, in this case, non-billable.
If you have some tasks on project that are billable and some non-billable, you can choose their billable status by enabling task rates in workspace settings.
Who can see and change billable status of entries #
You can set permissions so that only admins see billable status of time entries. This way, regular users won’t be able to see the currency symbol at all, and therefore, change the billable status of entries.
This option is in the Workspace Settings->Permission, and it is available if you upgrade to any paid plan. You can try out the feature for free by activating the free 7-day trial (no credit card required).
Historic rates #
When you change some hourly rate, that new rate will be applied only to new time entries you create from that moment on.
For example, if a team member’s rate is $20, and you change it to $40, all their existing time entries will still have the original $20 rate. But, if they create a new time entry (no matter for which date), that new entry will have the new $40 rate.
You can see each entry’s hourly rate when you hover over the amount in the Detailed report (as well as in CSV/Excel export).
Applying new rates to existing time entries #
Time entries pick up the latest rate each time you update project, user, or billable status of a time entry.
To overwrite previous hourly rate:
- Make the new rate apply retroactively to existing entries from the screen where you change the rate (any paid plan feature)
- Manually update time entries:
- Go to Time Tracker or Detailed report
- Click on the billable icon to mark entry as non-billable
- Click again to mark it as billable (this will reset their rate to the latest one)
- You can manually update entries individually, or do it via bulk edit
To prevent losing a historic rate, you can lock timesheets so regular users can no longer edit their old time or add time to the past. To prevent admins from making changes, you’ll need to approve time.