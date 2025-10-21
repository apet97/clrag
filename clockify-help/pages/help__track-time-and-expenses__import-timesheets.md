# Import timesheets

> URL: https://clockify.me/help/track-time-and-expenses/import-timesheets

In this article

* [Steps to import](#steps-to-import)
* [CSV file example](#csv-file-example)
* [Time formats](#time-formats)
* [Max character limits](#max-character-limits)
* [Important to note](#important-to-note)

# Import timesheets

4 min read

If you have historical timesheets data in Excel, you can import everything in Clockify as time entries, so your reports can include all your past and future data.

Import will create all the necessary [projects](https://clockify.me/help/projects/creating-projects#creating-projects), [tasks](https://clockify.me/help/projects/working-with-tasks), [clients](https://clockify.me/help/projects/creating-projects#managing-clients), [tags](https://clockify.me/help/track-time-and-expenses/categorizing-time-entries), [time entries](https://clockify.me/help/getting-started/clockify-glossary#time-entry) and their [custom fields](https://clockify.me/help/track-time-and-expenses/custom-fields) – all you need to do is provide the file.

Importing time is a paid feature, which you can enable by [upgrading](https://clockify.me/pricing) to any paid plan**.**  If you don’t have a subscription, only projects, clients, and tasks will be imported.

User interface displayed in this video may not correspond to the latest version of the app.

## Steps to import [#](#steps-to-import)

1. Navigate to the workspace name at the top left
2. Open the menu
3. Go to the **Workspace settings**
4. Choose **Import** tab
5. Prepare and upload CSV file (you can export CSV of Detailed report in Clockify to see how the file should look like)
6. Clockify will analyze how many entries will be imported (and how many [new projects or tasks will be created](https://clockify.me/help/projects/import-clients-projects) if you’re missing some)
7. Review information and click **Start import**

![](https://clockify.me/help/wp-content/uploads/2020/10/import-timesheet.png)

## CSV file example [#](#csv-file-example)

You can export CSV of Detailed report in Clockify to see how the file should look like,

[Download example CSV file](https://clockify.me/help/wp-content/uploads/2020/11/time-import-example-file.csv)

```
Project,Client,Description,Task,Email,Tags,Billable,Start Date,Start Time,Duration (h)
PTO,Sol-Tech,Time off,Vacation,james.white@gmail.com,,No,08/31/2019,9:00 AM,8:00
GS-100 Administration,Global Solutions,Feature development,Development,dale.the.knight@gmail.com,,Yes,08/31/2019,9:00 AM,8:00
CT-200 Banking app,California Tech,Troubleshooting,Support,ethel.rose.parker@gmail.com,,Yes,08/30/2019,4:00 PM,1:00
CT-200 Banking app,California Tech,Wireframing,Design,yvonne.gardner.ivy@gmail.com,,Yes,08/30/2019,3:00 PM,2:00
GS-100 Administration,Global Solutions,Answering tickets,Support,ethel.rose.parker@gmail.com,€,Yes,08/30/2019,2:00 PM,2:00
```

## Time formats [#](#time-formats)

Make sure the formats (time, duration, date) in the CSV file and your account match each other.

For example, if the start time in your CSV file is 1:00PM, but your account shows 13:00, the import will fail. You’ll have to either change the time in CSV to 13:00, or go to your Profile setting and change time format to 24-hour.

* **[Duration format](https://clockify.me/help/track-time-and-expenses/duration-format)** – you can change it in Workspace settings (hh:mm:ss, h:mm, h.hh)
* **Date format** – you can change it Profile settings > Preferences > [General](https://clockify.me/help/administration/profile-settings#general-settings) (DD/MM/YYYY, MM-DD-YYYY, etc.)
* **Time format** – you can change it Profile settings > Preferences > [General](https://clockify.me/help/administration/profile-settings#general-settings) (12-hour, 24-hour)

## Max character limits [#](#max-character-limits)

* Description: 3,000
* Task: 1,000
* Project: 250
* Client: 100
* Tag: 100

## Important to note [#](#important-to-note)

* Only admins can import time entries.
* You can perform an import action for an unlimited number of times, but the **file size is limited to 1MB**.
* You can import time **only for users on your workspace (active, inactive, or invited)**. User’s email in Clockify and their email in the CSV file have to match.
* [Limited members](https://clockify.me/help/track-time-and-expenses/limited-users) (users without email) are currently not supported.
* Required fields for time import: Email, Start date, Start time, Duration.
* Optional fields for time import: Billable, Description, Project, Task, Client, Tag (if some [required field](https://clockify.me/help/track-time-and-expenses/required-fields) is enabled, it is required in CSV too).
* If you don’t group projects by client, you should rename the client column in the CSV file accordingly.
* Duration in the CSV file should match the selected **Duration format** in workspace settings (**hh:mm:ss** or **h:mm**).
* Values in **Start time** and **Start date** columns in the CSV file should match your start and date formats from your [profile settings](https://clockify.me/help/administration/profile-settings).
* **End date** and **end time** are calculated automatically based on start time and duration.
* Time entries are imported according to the time zone of the person who does the import.
* If you don’t specify an entry’s billable status, it will be inherited from its project.
* Hourly rates are inherited [according to the hierarchy](https://clockify.me/help/reports/hourly-rates).

### Related articles [#](#related-articles)

* [Create projects & clients](https://clockify.me/help/projects/creating-projects)
* [Use tasks](https://clockify.me/help/projects/working-with-tasks)
* [Time categorization & tags](https://clockify.me/help/track-time-and-expenses/categorizing-time-entries)
* [Custom fields](https://clockify.me/help/track-time-and-expenses/custom-fields)

### Was this article helpful?

Submit
Cancel

Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me