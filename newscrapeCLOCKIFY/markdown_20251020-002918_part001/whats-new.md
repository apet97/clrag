# whats-new

> Source: https://clockify.me/help/whats-new

Team filters – Apply filters on the Team page to customize the view and quickly find specific team members, edit their profiles, or assign roles
Pumble integration – Receive messages on Pumble for the status of your submitted timesheets, time off balance or requests, and reminders to log or submit time.
Budget forecasting – Forecast whether you will go over the estimated budget.
iOS – Manage Time off requests from your phone.
✅ Fixes
Time off days not crossed out when creating or editing assignments
Exported balance report not showing an hourly time off policy assigned to a group
Error 400 appeared on the Assignments report after clicking ‘Show users without time’
User not automatically verified if signed up with SSO through the email link
Error 500 on the Schedule/Team page after Holiday assignees are changed to ‘Everyone (including new users)’
Timesheet template not applied in case time was created through timesheet and workspace has custom fields
Bulk edit on project’s rates displayed correctly only after refresh
Custom fields with select options not loading on the Time Tracker page
Custom fields on random entries in Detailed Report do not show all options
Multiple visual and functional Approval page bugs
Project Managers redirected to their time tracker when approving timesheets
Project alert sent every hour
Numerical value for the User Custom Field disappears after saving
Banned users can log in and use the app
PDF of a Summary Report grouped by ‘Group/Project/Task’ shows empty pie charts
Time off requests not displayed correctly on the Approval page
The user cannot start the timer on the favorite project if he previously tried to add manual time entry without the required project
When ‘Force timer’ is on, we can edit everything except start/end time on the Time tracker and Calendar page, but the same thing on Timesheet is disabled
Team Manager not seeing “Approvals” in the sidebar
Regular users able to see and click on checkboxes next to names on the Team page
Kiosk login page visible even though the Kiosk is disabled in the workspace settings
Duplicated entries shown twice in the suggested entries list
Regular user can’t track progress on a private project with task, even if he has access to that project (via user group)
August 2024
🆕 Features
Paid CAKE.com Add-ons – Developers can now create and release paid add-ons for other Clockify users
Week start adjustments – Owners or Admins can now set week start day on a workspace level for all workspace members
✅ Fixes
Starting a timer on “Most tracked activities” in the Dashboard returns an error
Last month’s expense report empty when exported to PDF
Shared reports do not display clients attached to projects
New policies not applied to a user after changing their Group
Project Manager unable to create a new project from a template
User able to add time to a private project that they are not a part of
Total amount incorrect when using Compound Taxation mode in the ‘Send Invoice’ modal
Regular users, Project or Team Managers able to create time off entry by clicking ‘Play’ on a previously created one
Users not set in alphabetical order on the project Access tab
‘Group by’ filter in the Summary Report showing multiple rows for the same group
Adding a user as a Project Manager to all projects is not being accepted by the system
Creating two same reminders possible through editing previously different ones
400 status code when updating currently running entries and custom fields are not copied on autocomplete
Invoice with compound taxes not displaying correct balance after partial payment is recorded
QuickBooks: User getting Sync_fail error while sending entries from Detailed Report
User unable to change email address while 2FA is active
Admin not being able to import a CSV file
User status filter not working on time off requests
Team manager unable to add time entry in the Timesheet for one user
Time off request date filter not working as expected in the -6 America/ Regina time zone
User can see a project status even if the permissions ‘Who can see project’ status is set to ‘Admins’
Changing Project/Client/Task name not reflected everywhere on the Workspace settings page
Wrong redirection under “your profile settings” link for 2FA setting
Users are not able to change the entered e-mail address in the ‘Send Invoice’ modal
User displayed on the date range when they do not have an assignment
Assignees filter on Holiday policy showing only Groups
A dash not displayed when entering 0, 0.0, or 00 in the rate field
Apply multiple timesheet templates – Combine time and activities from multiple timesheets templates to quickly populate your daily and weekly timesheets
Improved overtime column in Attendance report – Overtime column in Attendance report now only shows values greater than zero. Work column includes a warning symbol for users who worked less than their capacity, with a hover message showing how many hours are left to work.
Searching by Groups within the Team page
✅ Fixes
Can’t export time off requests
Discrepancy in hours in automated weekly reports
Expense amount in audit log doesn’t reflect when unit price in expense category is updated
Some time entries don’t pick up default custom filed values
Tracked time on a project is not updated after that project is removed via Calendar
Clicking on a user’s approved request in Archive doesn’t work
Some approved time off requests don’t show up on time off timeline
Custom field number disappears when pasted
When OAuth is enabled via Okta, workspace login gets locked
Holidays for deactivated users show up in time off timeline, creating clutter
Regular user can’t change task’s billable status (if they have that permission)
Unsubmitted time tab in Approvals doesn’t list users who don’t have time but have expenses
API: /users/info not returning all users in special cases
Users not getting email to verify their account after accepting workspace invitation
User can not download expense reports through invoice mail while on a subdomain
Double toast appears when you profile name or photo is empty
Workspace cost rate accepts blank value
Data duplication in user custom fields
Add members popup is stuck when adding multiple members
Regular user can add themselves as a task assignee
When you create a new project, you can’t edit project details without first refreshing the page
Bulk editing projects’ amount to “0” doesn’t work on the Project page
Kiosk link invalid after 24 hours
Archived tags removed from existing entries
Reports filter for tasks shows private projects/tasks to managers not managing the private projects
Exported Report contains filtered values even though the user has not clicked “Apply filter”
Time Off Request Approval link redirects the Admin to the wrong workspace
Users able to save time entries longer than 999h by splitting long-running time entries
Tag dropdown not showing pagination
Company holidays not blocked out on the Scheduling page
Limited Users tab disappears on the Team page upon entering an invalid name in the search box
Running a timer through the Play button on the Dashboard page not working properly
User unable to log in to the workspace after the Data region transfer
Workspace still locked after Data region transfer
User unable to activate the Kiosk through the Kiosk page
Today’s time entry saved on yesterday’s date
Scheduled report link opens a blank page
Holiday not included in week’s capacity
Searching for limited users cannot be done by name
Time Off Balance and Request export shows deactivated users
Working days not exported for users added a long time ago
Alerts sent and counting all tracked time on a project disregarding monthly budget reset
Report showing blank page when exported as PDF
Decimal numbers cannot be imported into custom fields
June 2024
🆕 Features
API: List out information about limited users
Added ‘Test configuration’ button for SSO setup, both Saml2 and OAuth2
Passwordless login for Kiosk (log in via 2FA email code)
✅ Fixes
Wrong color of a chart in the ‘Group by’ section when the Summary report is exported in PDF
Hourly time off request displayed in two time zones to an Admin due to different time zones of the requester and Admin
Filtering Detailed Report for custom fields ‘smaller than’ and “larger than” values does not show results
A difference of 0.01 between the amount on the Expense page and the amount on the Approval page
Unable to verify the pending email change, if the user has a pending invite to a workspace
Screenshots on Mac and Windows not displayed correctly
Alerts emails arriving delayed and only at hh:30
Team Manager sees Task filter on Assignments report
Amount column does not disappear when the “Hide amount” option is selected in the Detailed Report
Enable 2FA button on the Force 2FA popup not working
Scheduled shared report emails show 0 as billable time
Workspaces in transfer able to install add-ons
Excel export doesn’t follow the date format
Restarting a time entry adds additional time to other time entries
User unable to stop the timer – permissions error
Ongoing timer lagging or frozen on the Time Tracker page
May 2024
🆕 Features
Time off entries – Create time entries from time off requests so they appear in time reports
Enhanced topbar navigation (there you can now find Workspace Settings, workspace switcher, app switcher, and subscription management)
UI updates: New styles of the Status and Alerts banners
✅ Fixes
Marking an entry as a break in Detailed Report not possible if the Project field is required
Editing duplicated time entries reverting to original value on slower networks
Assignments made after March 31st appear as scheduled a day later on the Calendar’s header
Daily time tracking reminder sent to a user on their time off day
User unable to turn time entry into break entry in the Detailed Report when the project is a required field
PDF Expense report not containing existing expenses with an archived/deleted category
Users unable to save multiple Workspaces with the same name, or name a Workspace with a single character
Recorded GPS locations at the bottom of the Activity list cannot be deleted
Time entry with quotation marks in the description exported from a Detailed report in CSV shown as two separate fields in the pivot table
Detailed report export in CSV or Excel always showing a ‘Type’ column
Reactivated users not able to clock in to a kiosk
Filtered tasks/projects not displayed in the dropdown after the dropdown has been closed and reopened
When lock time before “today” is enabled, the user can create an entry that was started before “today”
Audit log showing wrong custom fields for displayed time entries
Duplicated estimates fields on the exported Summary report (CSV, Excel)
April 2024
🆕 Features
Split time – Create two separate time entries from one
Data region transfer – Transfer data from global to regional servers, or from region to region
CAKE.com Bundle plan – Get time tracking, project management, and team communication app for a special price and save 53%
Export team data – Download a list of all your members and their details in CSV & Excel
✅ Fixes
Date on the Tracker page shows a day behind if a timezone is set to Pacific/Auckland
Automatic accrual of days under a specific Time off policy with disabled accrual
Editing entry’s start time on a workspace with h:mm time mode changes the end time by one minute
Admins able to allow “Require 2FA” after clicking on a resend code option
Time off balance for a specific user is not updated correctly after an time off request on desktop
Asia/Almaty time zone displayed incorrectly (+1 hour)
Favorite tasks not listed on top when creating an entry in the Calendar
Unsuccessful import of a file with archived tags to a workspace where tags are a required field (Chrome, Firefox, Safari)
Exporting members from the Team page resulting in “Download failed” error after loading
Attendance report page infinitely loading
Regular user unable to save a project as a template
Navigating between custom fields with the TAB button while the timer is running sends the cursor to the first field after each successful save
Changing expense date does not trigger changes in project status
Regular users able to change task assignees or delete tasks via API
Admins whose Day start is set to 22h don’t receive tracking reminders
Sorting on the Accounts tab in Workspace settings not alphabetical
Prevented double time off requests on slow networks
Durations on exported Summary and Detailed PDF reports rounded on two instead of four decimal points
Renamed label for “Projects” not reflected on the Scheduling drop-down menu
User able to change the billable status of Expenses even after the option for billable hours is deactivated
Kiosk logs out after 24 hours even though is set to expire after 999 hours
Users able to mark a required custom field as invisible after making it required
Searching by email on the Team page does not return any results
Regular users unable to add time to private projects they have access to, after copying last week’s timesheet
Time off policy report exported from the Balance tab showing user removed from that policy
Exported Team report does not show groups for users who have another active workspace
Break column not visible in the exported Attendance report
March 2024
🆕 Features
Favorite entry – Pin favorite time entries to the top for a quick start
Group the Assignment report by groups
See available hours (based on user’s capacity) in the Assignment report for users or groups
Differentiate between regular time entries and break entries in your reports
Expense report sent via invoice email now requires a PIN code to access, for added security
✅ Fixes
Admin can’t return to a Kiosk start page when launching a Kiosk they’re not part of
Marking tasks as required during a “Clocked in” session on a Kiosk, shows users the “Clocked in” screen when switching tasks instead of the “Switched project” screen
Filtering “Inactive” users on Time Off tabs doesn’t show a consistent list of users when switching tabs
Cloned time entry created in the Calendar page by dragging not counted in the tracked column of that project’s progress page
Changing start week to a different day doesn’t reflect in the date picker of an already created shared report
Setting the Project’s member rate as 159.14 changes it to 159.13 when returning to the Project’s Access page
List of payments in Invoices displaying the default Workspace currency instead of the specific currency for that client
Yesterday’s date does not appear crossed out when creating or editing a time entry for regular users after admins lock time before “Today” and then enable Expenses
Task disappearing from the schedule when switching between the Projects and Team tabs on the scheduling page
Added task budgets not visible after switching from the Tasks tab to the Progress tab until the page is refreshed
Project budget estimate showing its previous value in the Status tab after its been set to zero, or after its been turned off and turned on again
Bulk-selecting projects or archiving a project in the Projects tab sets their time estimate to zero until the page is reloaded
Running time entries in the Calendar missing the stop icon
Two time off badges displayed in the “Planned” section of the weekly Calendar view instead of one after a user makes a time off request for today
Project template dropdown not responsive if a user does not have any project templates
An infinite loader displayed on the Time off page on the balance tab when all policies are archived
Specific receipt showing up on the next page when a PDF Expense report is exported
Project time estimate different in the exported Summary report from the one in the project status tab
Entries imported via CSV file not having the “Import” label in the Audit log
Timesheet withdrawn email showing a random regular user as withdrawer after the approval period has been changed by an Admin
Client picker not listing all the clients while creating an invoice, if there are more than 50 clients in the workspace
User dropdown not listing all the users in the Detailed report while bulk editing, if there are more than 50 users in the workspace
Pie chart in the project status tab showing time estimate instead of a budget estimate, when the user sets the budget estimate manually
Timesheet columns and table header misaligned on higher zoom and when tags are a required field
Removing a project with a task on an existing time entry in the Detailed report displays that currency type as “null” before refreshing the page
“Delete screenshots” modal not showing correct subtracted time after a regular user deletes a screenshot
Active users converted to inactive users able to access shared reports
Start time in GPS tracking recorded twice
Unsubmitted expense not present on the Approvals page/Unsubmitted tab if the Admin has already approved time entries and expenses for the same period
Incorrect number of visible custom fields while moving fields from available to visible column, and vice versa
Project manager can add milestones to private projects they don’t have access to
Task with a duplicated name saved until the page is refreshed, or until rates are changed
February 2024
🆕 Features
Schedule tasks – Plan tasks and your team’s labor hours on a timeline.
Kiosk launch settings – Allow managers to launch a kiosk, or turn off login requirements in workspace settings so anyone can launch it.
Bulk archive/delete clients and tags
Start breaks via API
✅ Fixes
Team Managers can see Team Dashboard for members that are not in their team
Clicking on the Timesheet field shows the decimal value multiplied by 100
Attendance report not sorting correctly by date
Assignment report not sorting projects alphabetically and months chronologically
Entry duplication errors when hitting the Add button multiple times
Owner’s time entries created via kiosk are always marked as non-billable
System can send entries to QuickBooks that are longer than QuickBooks’ maximum duration and that have been already sent
Time Off policy assigned to a group doesn’t apply to all members of the group
TaskID error showing up when adding a user to the schedule
Custom fields refusing to set as “no value” after deleting a previously set value
Not enough details in error message when CSV import fails
Can’t import CSV file on Windows 10 Firefox
Projects with special characters (<, >) can’t be deleted without removing the Note
Incorrect balance and status on old invoices created before the partial payment feature
Spellcheck not working on some pages
Unable to go back from project budget to time estimate if a time estimate is set
Turning on/off 2FA in Profile settings logging users out
The project template doesn’t apply assigned manager roles while creating new projects
“Copy as time entry” from Calendar events not working for regular users
“Filter by Access” on the Project page doesn’t recognize group-assigned projects
Custom colors don’t apply to projects
Moving and resizing entries in the Calendar opens a pop-up to edit an entry instead of moving it (Firefox)
Summary Report not showing correct graph for a 1-year time range
Expenses list not showing up in the PDF report
Time entry updates made through a Calendar are not saved
Regular users can’t create entry via Timesheet on private projects
Tasks can be deleted by their project managers even though the “Who can create tasks” permission is set to “Admins”
Users able to set a password using blank/space characters
“Download Failed” pops up when exporting Excel or CSV of a Detailed Report including “Employee ID” as an active custom field
Unable to add a new project on the Scheduling page when it tries to load too many projects
January 2024
✅ Fixes
Missing translations on some pages
Filtering members doesn’t work if members are added via project’s Access tab
When selecting a project from the Description field on the Time Tracker page, the custom field doesn’t populate with its default value
Calendar not showing the correct date after being in “sleep mode” for one or more days until the page is refreshed
If a time off request is approved in one time zone and then changed to another, the calendar and scheduling pages show two time off days instead of one
Project monthly estimate not including time entries that have same start time as start time of estimate
Field formatting error when copying and pasting task budget number to another
“Verify email” banner is displayed for already verified users
Downloading an invoice in Hebrew inverts descriptions
Improved invoicing (group by project/user/date & subgroup by project/user/date/description, get user in detailed time import, add Tax 2, enter negative value in quantity and price, more decimals for tax value)
Get each user’s group in Detailed report’s CSV/Excel export via customize export
Add team member without triggering email invitation
What’s fixed
When amount and user is disabled in Detailed report’s customize export, PDF still shows User in the column header
Various Calendar bug fixes
When creating time via Timesheet’s detail view, changing billable status isn’t remembered
Timesheet import via CSV doesn’t work when if start/end misses seconds and displays wrong message
Team managers can’t see Team Dashboard
Team managers can’t see their team members without time in the Weekly report
Team manager can’t filter report to get only their time
Screenshots and locations aren’t automatically deleted when timer is canceled
Admins can’t edit or delete rows in Timesheet for completed tasks or archived projects
When a user is removed from a workspace, their timer for the workspace is not discarded
“Expand all” options on Projects page (mobile version)
Added “Without task” on project status
Completed tasks are visually marked on project status page
Added “Overage” on project status
Project name appears in browsers tab’s title
What’s fixed
Timesheet template tasks not being saved
Project cost rate is reset when project estimate is changed
Regular users see dollar icon on Time tracker even if the workspace currency is different
Sometimes “No client” in the project picker appears down the list
Lazy loading
Project templates list all projects
Project managers can’t see status overview for any project
Some entries without description are not grouped together
Missing filter button on Projects page on smaller resolutions
Color picker opens on Enter when saving manual estimation
API pagination on Detailed report doesn’t work
Alerts for task-based estimates don’t come out right
Sorting order in project picker is not good in some cases
Can’t create more than 10 webhooks on a workspace
It’s possible to approve time entry in progress
Users from groups who have access to private shared report can’t open it
Some users can’t seethe workspace they are a part off
Problem when submitting for approval in time zones affected by daylight saving time
In Approval details, some billable entries are shown as non-billable
Can’t expand projects in timesheet
On approval withdraw, “Review timesheet” link in emails doesn’t work
When changing time zone through the “time zone mismatch” notifications, pending approval requests are not withdrawn
Cost rate in Approval details are calculated only if a project is billable
Admin cannot see some user added to a project
API doesn’t send content-type for PDF, CSV, and Excel reports
Can’t select all users when bulk editing users to projects
Sorting projects in project picker is not good in some cases
When adding users to a project, all users are listed instead of just active ones
When adding users to a project, changing filter resets the selected users
Tooltip doesn’t display full project name on hover
Deleted project doesn’t immediately disappear from the list
Missing active/archived selector in client filter on Projects page
Missing active filter indicator on Projects page
Status page doesn’t show estimated tasks when there’s a new hourly rate (needs refresh)
Missing “Restore” in project bulk edit
Missing copy when there are no more members to add to a project
July 2020
What’s new
Time approval
Prepay user seats for Enteprise plan
Complete API documentation
Sort Team page by group
Week total on Time tracker
Active filters on Project page are remembered
Both members and groups are shown in project access tab immediately
Dropdowns on Reports are open on hover
What’s fixed
When Time tracker is left open overnight, date says “Today” even though it will add time to yesterday
Admin cannot see a user added to a project
Deleted client appears in project picker when collapse is turned on
Sidebar glitch on iPhone and other visual issues
Cost rate on project isn’t shown even though it’s saved and applied
If Team page is hidden, regular users and managers can’t see their name in Team filters in reports and can’t click in table on user name to filter the report by the user
Regular users can’t access get their time entries using /time-entries endpoint in API
Missing “content-type” in Reports API’s header
Changing duration in Timesheet doesn’t update end time incrementally, as according to profile settings
Can’t create webhooks on subdomain
Sort on Dashboard is not case-insensitive
Owner can remove their role from Group page
It’s possible to create two projects with the same name and the same client via bulk edit
Missing toast message when activating/deactivating users
Missing total time in Weekly report PDF
Tag filter is not working properly in some cases
“Select all” in task filter selects only first 50 tasks
“Copy invite link” on subdomains is not right
High CPU usage on log in page
Webhooks don’t return user’s name
Selected tag doesn’t show up immediately
Sometimes a user is both active and pending at the same time on subdomain workspace
“Fix” link on Timesheet doesn’t apply proper filters in Detailed report
Project picker sometimes doesn’t display projects/tasks
When there’s no project selected, project picker still offers “No project”
Unclear copy when filtering primarily by task
When adding users, captcha appears after entering emails
Missing confirmation dialogues when deleting some stuff
Time grouped by date isn’t sorted correctly in PDF export
Summary report and PDF aren’t consistent when grouped by User/Task
Reset password link should be expired after 2 hours
When task is a required field, you can’t see projects that don’t have tasks
When you open a link but you’re not logged in, after logging in you’re not redirected to the original page
Sometimes you can’t see who is Project manager when you open Access tab on a project
Admin can’t change hourly rate for users who have not joined yet
Setting workspace hourly rate sets the same rate to users who don’t have an hourly rate
In progress entries are not shown on Dashboard
Can’t download PDF on Safari
Project manager can change duration for others in Detailed report (but change is not saved, which is ok)
Adding user group to a project requires refresh to display the change
Summary report groups projects with the same name even if they have different clients
Summary report groups tasks with the same name even if they are on different projects
Entries admins add for others are not locked
Editing start and end time in Detailed report doesn’t work like on Time tracker page
Admin can’t modify user groups owners created
Wrong time gets added in manual mode if you click on ADD immediately after typing end time
Play button on locked entries is missing
When you go to some other workspace’s settings, your active workspace is not changed
Reset password link expires too soon
Doesn’t show that you’ve removed admin role from someone until refreshing the page
Can’t change project members’ hourly rates for projects made from templates
In manual time entry mode, if you enter start or end time and click “ADD” without moving the focus away from the time field first, the row gets added with wrong time
When you load more projects in Dashboard, new projects are sorted incorrectly
Users can’t access a project if they’re added via a user group
Clicking on sidebar doesn’t close the notification popup
Time zone mismatch notification for some time zones doesn’t work properly
Time zone label in Personal Settings is not accurate for some time zones
When bulk editing projects, “Select client” becomes the name of the client
When you signup but already have an account with that email, a new workspace with the same name is created
Custom value of project grouping label isn’t reflected in Bulk Edit
There’s no indicator to wait while Clockify is exporting a report
April 2019
What’s new
Brand new PDF exports (download samples)
Brand new Time Tracker
Bulk edit in time tracker
Group same time entries
Responsive design (works on all screen sizes)
Create projects and tags from time tracker
Compact project list
Duplicate creates an identical entry
Move entries to a different workspace
Description field max length raised to 3,000 chars
Add time by duration in manual mode
Show 50/100/200 entries per page
Keyboard shortcuts (n, c, s, m)
Improved controls and performance
“Filter primarily by: Task” can now also search by client (task @client)
Create task and project from project picker by typing “task@project”
Choose between project and billability chart in Dashboard
See all running timers in workspace
See when was someone last active
See your preferred currency symbol in charts
Automatic update of lock dates
What’s fixed
Continue timer button doesn’t pick up project/task field if a user is added on that project via user group
Can’t scroll down user groups list when saving a report
When you select an older date in manual mode and add time, the date reverts back to today but the calendar says it’s the same the same old date
Yearly reports don’t work right in some time zones
In templates, completed tasks are not copied
February 2019
What’s new
Active workspace is now displayed in sidebar under the user’s name
Random project colors are now assigned when you create a new project
On Projects page, Team column displays Anyone if a project is public
Notification improvements (auto-open, open/close on click, clear all, design, removed discarded notifications, new notification when you’re deleted from workspace, invite notifications always appears on top)
Archived projects now appear crossed out on Projects page
You can now open projects in a new tab from the Projects page (either via right-click menu or on middle click)
Print button automatically downloads print-ready PDF
Success message when updating billable/non-billable time
What’s fixed
Detailed report sends you to 1st page on edit and sorts the entry as soon as it gets a new value (so you lose track of the thing you’re editing)
Long user name in sidebar isn’t shortened
Entering time using space is not working (e.g. 4 am)
Project picker doesn’t always properly sort by client name
Total hours missing from saved reports
Project page throws a lot of “Project updated” message when changing custom color
When data is deleted form some project, Timesheet saves that project’s name
Task’s row remains in Timesheet when you delete the task
A project’s tracked time is different on the Projects page and on the project’s Status
When you’re on Workspaces page and you create a new workspace, you’re not switched to the newly create workspace
When deleting a “net joined yet” user, message doesn’t display user’s email
Project status’ billable/non-billable chart has random colors
When you create new time entries for others, entries don’t appear on top
Time entries assigned to wrong client in the Detailed report if the project has the same name
Project status is not updated after you delete time
When changing password, there is no message that says that the old password is required
Sometimes the start time resets to 9am
Edit tag pop-up opens up for locked time entry even if you can’t edit the entry
Detailed report doesn’t sort well by duration when seconds are turned off
Selecting a custom date makes the timesheet move entries by one day
Label for Project manager sometimes doesn’t appear
Entered hourly rate doesn’t recognize comma as a decimal separator (only point)
Reminder with lots of users doesn’t display properly
Exported report doesn’t reflect sorting
Invalid date on web in manual mode when the timer starts running in apps/extensions
Project manager permission is not removed when a user is removed from the project
When you enter hourly rate or manual estimation, success message is missing
Filters on Projects page are removed when you delete/archive a project
When editing tasks on projects, “Show only active tasks” switch reverts to ON
Can’t see completed tasks on Safari & Edge
“Without project” color in reports is always random
Project colors in pie charts are randomized on hover
Manual time entry mode and offline support for Android/Windows/Linux app
Better start/end timer sync between all the apps
You can now search by client name in project dropdown filter (not possible if smart filter is turned on)
Project’s client is now shown in the Timesheet
What’s fixed
Entries for a completed task disappear from the Timesheet
Filtering by client on the Projects page doesn’t work
Weekly report doesn’t list subgrouped properties properly
Projects with the same names are combined in reports and timesheet
When we add a new project in timer mode, and switch to the manual mode, the project disappears
When we edit the time entry and use smart project filter, and after that use tag, the project disappears
Every time we click on some project, “Project updated” message appears
Create a new project from timer page doesn’t work well if we already have some time entry
A non-admin user can see time entries of another user if they choose to see archived projects in a report
Other users see task which are assigned to someone else on public projects
Can’t see who is workspace owner
If project favorite is enabled, search bar shows all projects as favourite
If Tag is a required field, “no tag” is allowed for editing old time entries
Hourly rate for time entries without a project doesn’t show in Summary report
Editing project in timesheet adds a new row
Commas aren’t escaped in task names when exporting reports in CSV
Play button doesn’t copy the project if you’re not part of the team
“Without client” filter on Projects page doesn’t work when changed
Dashboard chart does not match project colors
Favorite projects don’t show client names
Favorite projects don’t work well with project filter
When you invite to workspace someone who already has an account, they don’t show up on the Team page until they accept the invite
When a user is added to workspace, they are not shown until you refresh the page
When a user is invited, they get a confusing page which only says Password
Copy last week in Timesheet doesn’t work properly
September 2018
What’s fixed:
Project/Task filter is too finicky
Weekly report email doesn’t follow “Week start” day defined in User Settings
When adding a tag in the Detailed report, the tag popup freezes
If a user has one workspace, every time they login or go to workspaces page it throws toast for default workspace change
When we enter time in a timesheet for e.g. 4th and 5th September and in calendar chose those days, it will move hours for the next day. When we refresh the page it will be good again.
Zero hours is showing in timesheet page (when a time entry with zero hours is added on Time tracker page)
If we check Public on a project, then add an assignee to a task, and then check out the public, assign for that task will be empty
When adding a time entry with a required field, the description is gone and tag can’t be added anymore
Need to reload the page to see workspace invite notification
Add Members in a project’s page doesn’t work properly
Time entry can have a task which doesn’t belong to a specific project via API
When the timer is running, “Give manager rights” isn’t clickable in the project team page
Favorite projects aren’t affected by the filter
Estimate progress on a project are not shown until you have tracked some time
Reminder coming for the day which isn’t checked in the days list
Duplicated projects in the report filter when unchecking client filters
Allow same project name if you have different clients
What’s fixed:
Inactive/deleted user can’t track time because they have no other workspace
The dashboard shows other users’ entries
“Stay logged in” isn’t checked by default when using Google login
End timer button is the same color as for starting the timer
Targets block shows up in User Settings even when there are no targets
Deleting locked entries in Timesheet causes some issues
The whole week is locked in Timesheet if even a one day in the week is locked
Entering a future date for the running timer results in bad calculation of duration
No Project doesn’t show on some workspaces
The project field remains a required field when Timesheet is disabled
Invitation link doesn’t work properly if an account already exists
The total time for that day is not entered after the timer stops (need to refresh the page)
CSV export of a report is missing a column with time in decimal format
Updating time entry in the Detailed report doesn’t work when “Do not allow saving time without project” is turned on
In timesheet, you can add the same project more than once
Adding project/task after adding durations on timesheet page is disabled
When the timer is running, date picker doesn’t work
Time from archived projects disappears from the Time tracker page
When you add a time entry with a tag, the tag will stay in place for the next time entry
Error message appears in the console after click on the “X” for the running timer
Time entry end button doesn’t work properly in some cases
When you write a description for a time entry and then click out of it, a new notification pops up in green “Successfully updated time entry. If you have clicked another time entry and are typing its description, the notification pops up and stops you from typing
Improved Weekly report (more details and breakdown, a total column for each day, client name next to project)
Delete and manage invited users who didn’t accept the invite
What’s fixed:
When you set user as inactive, their hourly rate is lost
Delete inactive user doesn’t work
Dropdowns are not closed when switched to another field using Tab
Dashboard includes the time from the current running timer
March 2018
What’s new:
Mark tasks as done
Remove a user from a workspace
See timer running in the browser tab
Change email
Delete account
Full export of Detailed report (clients, tasks, tags, and more)
Task name character limit raised to 1000 characters
Clockify automatically assigns you the correct time zone when you first sign up
Added YYYY-DD-MM date format
Only task assignee can select the task when tracking time
Time tracker page now shows ALL the entries you’ve made in the last 7 days (not just 10 most recent ones as before). On each “Load more”, Clockify loads one more week. To see (and edit) time entries older than 1 month, you should use Detailed report. Use ENTER key to confirm dialogs.
Time tracker page is much faster now ( even if you have hundreds of time entries)
Stay logged in longer (no more having to log in each day)
You can now delete time entries in Detailed report (admins can delete all and team members can delete entries that they made)
You can now see date of each time entry in Detailed report
Notification when the time zone is not set correctly
Sorting is now case-insensitive
What’s fixed:
Clicking on + doesn’t fold back tasks in the time tracker
Long time descriptions in PDF exports overlap duration and amount
Team member can’t edit their time entries in Detailed report
Tasks aren’t sorted alphabetically
Support menu can’t be seen on smaller screen sizes
Input box text is difficult to see
Can’t export a saved report
Completed tasks can’t be selected as filters in a report
Time entries that start on one day and finish the next shows up in a report for both dates. Now, that time shows up only for the day it finished
Sometimes, due to different time zones, reports show time entries for the day before
User group members can’t access the project
When you remove a user from a user group, time entries from that user on a project where that user group was assigned won’t show in reports
Hover menu on Reports disappears too quickly
Long workspace names aren’t displayed fully
There’s no error message when 1) adding a task with the same name 2) task name is too long
Error when updating task estimate for tasks that have the same name as tasks on other projects
Users who are not owners can’t see saved reports, even if they saved one
You can’t edit and select a different project in Detailed report
Infinite scroll on project list on Time tracker page
Filtering time entries by name is case-sensitive (e.g. searching “Recording video” doesn’t return results for “recording video”)
There’s no page when a password token expires and a user doesn’t know that they have to reset the password again
When “Who can see Teams Dashboards” setting is set to everyone, some users still can’t see Team Dashboard
Admin can’t change a user group when updating a saved report
There are two users with the same email in the system
Subscribe/unsubscribe button for newsletter doesn’t work