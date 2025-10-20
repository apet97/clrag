# track-time-and-expenses-duration-format

> Source: https://clockify.me/help/track-time-and-expenses/duration-format

Duration format
Efficient time tracking is at Clockify’s core, and we understand that different users prefer different ways of representing duration. With preferred duration format, you can see, enter, and export time in format that suits your needs.
Clockify has three different duration formats:
- Full (hh:mm:ss)
- Compact (h:mm)
- Decimal (h.hh)
How duration formats are implemented #
- Full: ‘2’ = 2 minutes
- Compact: ‘2’ = 2 minutes
- Decimal: ‘2’ = 2 hours
- All formats:
- ‘2h’ = 2 hours
- ‘2m’ = 2 minutes
- Full format only:
- ‘2s’ = 2 seconds; other formats show 0:00 for less than 1 minute
- ‘120s’ = 2 minutes
Decimal duration format (e.g. 2.5 hours) would be ideal for a freelancer who is invoicing clients based on hourly rates. This format simplifies the billing process and is useful to those who need time entries in a numeric form.
Decimal format is a paid feature you can enable by upgrading your workspace to any of our paid plans.
Set up duration format #
To set up duration format on your workspace:
- Navigate to the workspace name
- Open the menu
- Choose Workspace settings from the dropdown
- Find duration format in the General tab
- Choose one from the dropdown
Once you selected duration format:
- That duration format is displayed everywhere in the interface (tracker, timesheet, reports, invoices etc.)
- Duration in PDF/Excel and CSV report exports is in that format
- Cells in all duration inputs interpret time in that format (e.g. if you type 1, it is considered to be 1h)