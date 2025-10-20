# track-time-and-expenses-import-timesheets

> Source: https://clockify.me/help/track-time-and-expenses/import-timesheets

Import timesheets
If you have historical timesheets data in Excel, you can import everything in Clockify as time entries, so your reports can include all your past and future data.
Import will create all the necessary projects, tasks, clients, tags, time entries and their custom fields – all you need to do is provide the file.
Importing time is a paid feature, which you can enable by upgrading to any paid plan. If you don’t have a subscription, only projects, clients, and tasks will be imported.
Steps to import #
- Navigate to the workspace name at the top left
- Open the menu
- Go to the Workspace settings
- Choose Import tab
- Prepare and upload CSV file (you can export CSV of Detailed report in Clockify to see how the file should look like)
- Clockify will analyze how many entries will be imported (and how many new projects or tasks will be created if you’re missing some)
- Review information and click Start import
CSV file example #
You can export CSV of Detailed report in Clockify to see how the file should look like,
Project,Client,Description,Task,Email,Tags,Billable,Start Date,Start Time,Duration (h)
PTO,Sol-Tech,Time off,Vacation,james.white@gmail.com,,No,08/31/2019,9:00 AM,8:00
GS-100 Administration,Global Solutions,Feature development,Development,dale.the.knight@gmail.com,,Yes,08/31/2019,9:00 AM,8:00
CT-200 Banking app,California Tech,Troubleshooting,Support,ethel.rose.parker@gmail.com,,Yes,08/30/2019,4:00 PM,1:00
CT-200 Banking app,California Tech,Wireframing,Design,yvonne.gardner.ivy@gmail.com,,Yes,08/30/2019,3:00 PM,2:00
GS-100 Administration,Global Solutions,Answering tickets,Support,ethel.rose.parker@gmail.com,€,Yes,08/30/2019,2:00 PM,2:00
Time formats #
Make sure the formats (time, duration, date) in the CSV file and your account match each other.
For example, if the start time in your CSV file is 1:00PM, but your account shows 13:00, the import will fail. You’ll have to either change the time in CSV to 13:00, or go to your Profile setting and change time format to 24-hour.
- Duration format – you can change it in Workspace settings (hh:mm:ss, h:mm, h.hh)
- Date format – you can change it Profile settings > Preferences > General (DD/MM/YYYY, MM-DD-YYYY, etc.)
- Time format – you can change it Profile settings > Preferences > General (12-hour, 24-hour)
Max character limits #
- Description: 3,000
- Task: 1,000
- Project: 250
- Client: 100
- Tag: 100
Important to note #
- Only admins can import time entries.
- You can perform an import action for an unlimited number of times, but the file size is limited to 1MB.
- You can import time only for users on your workspace (active, inactive, or invited). User’s email in Clockify and their email in the CSV file have to match.
- Limited members (users without email) are currently not supported.
- Required fields for time import: Email, Start date, Start time, Duration.
- Optional fields for time import: Billable, Description, Project, Task, Client, Tag (if some required field is enabled, it is required in CSV too).
- If you don’t group projects by client, you should rename the client column in the CSV file accordingly.
- Duration in the CSV file should match the selected Duration format in workspace settings (hh:mm:ss or h:mm).
- Values in Start time and Start date columns in the CSV file should match your start and date formats from your profile settings.
- End date and end time are calculated automatically based on start time and duration.
- Time entries are imported according to the time zone of the person who does the import.
- If you don’t specify an entry’s billable status, it will be inherited from its project.
- Hourly rates are inherited according to the hierarchy.