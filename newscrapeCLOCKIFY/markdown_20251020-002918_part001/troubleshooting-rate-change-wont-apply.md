# troubleshooting-rate-change-wont-apply

> Source: https://clockify.me/help/troubleshooting/rate-change-wont-apply

The rate change won’t apply to time entries
If your updated hourly rate isn’t showing up in reports, it’s likely because something else is overriding it or preventing the update. Here’s what to check and how to fix it.
A more specific rate is overriding the one you changed #
Clockify prioritizes rates in the following order (from lowest to highest priority):
- Workspace rate
- Project rate
- Team rate
- Task rate
- Project member rate
More specific rates will override less specific ones. Even if you change the team rate, for example, the project member rate will take precedence.
What to do:
Check and adjust the specific rate that may be overriding the one you intended to change:
- Workspace rate
- Click on the three dots next to the workspace name
- Select “Workspace settings”
- Scroll a bit down and check the workspace rate
- Project rate
- Navigate to the Projects page from the sidebar
- Find the project from the list and click to open it
- Navigate to the “Settings” tab and check the hourly rate
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
The rate wasn’t applied to past time entries #
Even if you set the right rate, Clockify won’t retroactively apply it to past time entries unless you explicitly choose to do so.
What to do:
- If you’re on a paid plan, go back to the rate settings and check the “Apply to all past and future time entries” option when saving.
- If you’re on a free plan, go to the Detailed report, find the affected time entries, and toggle the billable icon off and on to refresh the rate.
The time entries are approved #
Approved time entries are locked, including their hourly rate. If a time entry is approved, rate changes won’t apply even if everything else is correct.
What to do:
You’ll need to withdraw the timesheet to unlock it and update it:
- Go to the Approvals tab from the sidebar
- Open the Archive tab
- Locate and click on the timesheet in question to open it
- In the upper right corner, click Withdraw
- Go back to your rate settings and update the rate
- Once the rate is correctly applied, you can resubmit the timesheet for approval
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and include the following details:
- Information about which rate you’re trying to apply
- Whether you’re on a free or a paid plan
- A screenshot of the rate settings you’ve changed