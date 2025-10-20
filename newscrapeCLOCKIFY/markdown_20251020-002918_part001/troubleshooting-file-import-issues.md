# troubleshooting-file-import-issues

> Source: https://clockify.me/help/troubleshooting/file-import-issues

CSV File import issues
If your CSV file fails to import into Clockify, it’s usually due to formatting issues or missing required data. Below are the most common reasons why imports fail and how to fix them.
Required headers are missing or incorrect #
Your CSV file must include the following required column headers, written in English.
- Project
- Client
- User
- Task
- Tag
- Start date
- Start time
- Duration
You can find the full list of supported columns here.
Headers must be spelled correctly in English, free of extra spaces or characters. If any of these are missing or incorrectly formatted, your import will fail.
Date, time, and duration formats don’t match Clockify settings #
Clockify reads your CSV file based on your account and workspace formatting settings. The start date, start time, and duration fields must follow these settings.
Date and time format:
- Click on your profile picture in the upper right corner
- Select “Preferences.”
- Under the General tab, check your Date and Time formats
Duration format:
- Click on the three dots next to your workspace name
- Click on the “Workspace settings”
- Under the General tab, check the Duration format:
- Decimal
- Full
- Compact
Your CSV file must match these formats exactly; otherwise, the file will be rejected.
Excel formatting issues #
If you opened or edited your CSV file in Excel, it might have changed the formatting (e.g., dates, times, or stripped leading zeroes). This often breaks the import.
To prevent that, we recommend opening and editing your CSV file in Google Sheets, which maintains correct formatting.
The file is not comma-delimited #
Clockify expects CSV files to use commas as delimiters. If your file uses semicolons instead, the import will not work.
How to check if your file is comma-delimited:
- Open the CSV file in a plain text editor (like Notepad)
- Check the character separating values:
- If values are separated by commas, the format is correct
- If you see semicolons (;), you’ll need to convert the delimiters to commas.
You can also open the file in Google Sheets and re-download it as CSV. Google Sheets will automatically format it correctly using commas as delimiters.
Missing or incomplete field values #
Even if all required fields are present, your import can still fail if some fields are left empty in your CSV file.
Check your workspace required field settings:
- Click on the three dots next to your workspace name
- Select “Workspace settings”
- At the top of the page, check if the Timesheet is enabled. If it is, Project becomes a required field by default
- Scroll down to the “Do not allow saving time without” section to see if additional fields (e.g., Description, Task, Tag) are marked as required.
If any of these required fields are empty in your CSV, the import will not succeed.
Custom fields:
If your workspace requires custom fields, you must also include those in your CSV, with valid data for each entry.
To streamline the import process:
- Temporarily disable all required fields in your workspace settings
- Import only the essential time entry data
- After the import, re-enable your required fields
This approach saves time and avoids needing to populate every single field in advance.
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and provide us with the following information:
- A copy of the CSV file you’re trying to import
- A screenshot of any error messages you’re getting when importing the file