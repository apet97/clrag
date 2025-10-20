# troubleshooting-invoice-total-is-0

> Source: https://clockify.me/help/troubleshooting/invoice-total-is-0

Invoice total is $0
If your invoice shows a total of $0, or no time entries at all, it usually means the time entries are missing a billable rate or weren’t marked as billable to begin with. Here’s how to find and fix the issue.
Non-billable time entries won’t appear on invoices #
Clockify invoices only include billable time entries. If your entries were tracked as non-billable, they won’t be available for import into the invoice at all. The invoice will appear empty.
How to check:
- Navigate to the Detailed report and select the relevant date range
- Look for the billable icon (dollar sign) next to your entries
- If the icon is grayed out, the entry is not billable
To fix it:
- Select the entries by clicking the checkbox next to “time entry’
- Select Bulk Edit
- Check the billable checkbox and toggle the button
- Save changes
After marking the entries as billable, return to the invoice and try importing again.
The hourly rate is $0 #
If your entries are billable but still not showing a total, the applied hourly rate is likely set to $0. Clockify will treat that as valid time with no cost.
Where to check:
- Project rate
- Navigate to the Projects page from the sidebar
- Find the project from the list and click to open it
- Navigate to the “Settings” tab and check the hourly rate
- Workspace rate
- Click on the three dots next to the workspace name
- Select “Workspace settings”
- Scroll a bit down and check the workspace rate
- Team member rate
- Navigate to the Team tab from the sidebar
- Check the Rate column next to each user
- Task rate
- Navigate to the Projects page from the sidebar
- Click on a project to open it
- Navigate to the Tasks tab
- Check the rate next to each task
- Project member rate
- Navigate to the Projects page
- Click on the project to open it
- Navigate to the Access tab
- Check or change the rate next to each user
A more specific $0 rate is overriding your intended rate #
Clockify follows a rate hierarchy, where more specific rates override more general ones. So even if you’ve set a project or workspace rate, a blank $0 project member or a task rate can silently override it, resulting in an empty invoice or a $0 total.
Rate hierarchy from lowest to highest:
- Workspace rate
- Project rate
- Team rate
- Task rate
- Project member rate
What to do:
Start by checking for any blank or 0$ rates at the top of the hierarchy (Task or Project Member), and work your way down. These will override the more general rates and lead to a $- invoice total.
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and include the following details:
- A screenshot of the invoice in question
- A screenshot of the Detailed report showing billable time
- Confirmation on which rates were set and where