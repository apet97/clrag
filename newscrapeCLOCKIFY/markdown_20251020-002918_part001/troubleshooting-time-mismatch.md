# troubleshooting-time-mismatch

> Source: https://clockify.me/help/troubleshooting/time-mismatch

Time and amounts mismatch in reports
If you’re noticing a mismatch in your reports, here are a few common reasons why that happens:
Compact mode is enabled #
- In Compact Mode, each time entry is automatically rounded to the nearest full minute for display purposes only
- This does not affect the actual tracked time; the system always stores time in the full format
- To view the exact time format:
- Navigate to the workspace settings by clicking on the three dots next to your workspace name
- Under the “Duration Format” drop-down, select “Full”
Once you switch to the full format, your reports will show you the most accurate data without rounding.
Rate hierarchy affects calculations #
Billing amounts may differ depending on how rates are applied. In Clockify, a more specific rate overrides a less specific one in this order:
Project’s member rate > Task rate > Project rate > Member rate > Workspace rate
- How to check which rates are applied
To identify where a rate is coming from, you can check each level in the rate hierarchy:
Project Member Rate
- Go to the Projects page and open the relevant project
- Navigate to the Team tab inside the project
- Check the rate column for each team member
Task Rate
- While still inside the project, navigate to the Tasks tab
- Check the rate column for each task
Project Rate
- Navigate to the Settings tab inside a project
- Scroll a bit down and check the rate
Team Member Rate
- Navigate to the Team tab located on the sidebar
- Check the rate for each team member under the rate column
Workspace Rate
- Click on the three dots next to the workspace name
- Click on the ‘Workspace Settings’ option
- Scroll down and check the workspace rate
You can edit the rates by selecting the ‘Change’ button located next to each hourly rate. If you are on a paid plan, you’ll have an option to apply the rate retroactively by selecting the ‘Apply to all future and past time entries’ option.
Discrepancy in Excel report #
If you’re seeing small differences in totals when exporting reports to Excel, this is due to how decimals are handled:
- The web app and PDF exports calculate the amounts using 4 decimal places, which ensures precise totals, especially when time is multiplied by hourly rates.
- When exporting to Excel, the data is sent with only 2 decimal places for display and compatibility reasons
- If you use Excel’s SUM formula, the totals may be slightly off due to rounding at the line-item level
Example:
A time entry amount of $33.3368 might appear as $33.34 in Excel. When summed across multiple entries, those small differences can add up.
For the most accurate values:
- Rely on the web report or PDF export, which reflects the true calculation using full decimal precision.
- Use Excel exports primarily for raw data or basic overviews
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and include the following details:
- A screenshot of the discrepancy in question
- A CSV copy of the report for the relevant date range
- Billable rate information