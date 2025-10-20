# troubleshooting-cant-submit-timesheet

> Source: https://clockify.me/help/troubleshooting/cant-submit-timesheet

I can’t submit a timesheet
If the submit button is missing on your timesheet, here’s what might be causing it.
Device time zone doesn’t match Clockify time zone #
If your device’s time zone doesn’t match what’s set in Clockify, the system may prevent you from submitting a timesheet.
- Look for a yellow attention sign at the top of the page
- Click on it to resolve the discrepancy
- Make sure your device’s time zone and your Clockify profile time settings match
Here’s how to change the time zone in Clockify:
- Click on your profile picture in the upper right corner of the screen
- Select “Preferences”
- Select the correct time zone from the drop-down under the Time Settings
Your timesheet includes entries linked to deleted projects #
If a project has been deleted, any time entry linked to it will now appear without a project, which is a required field.
- If that’s the case, you’ll see a warning at the top of the page
- Click Fix, and you’ll be redirected to the Detailed Report
- From there, you can assign a new project (if your workspace permissions allow it)
Your timesheet is empty #
If you haven’t tracked any time for the week, there’s nothing to submit.
- Add at least one time entry to enable the Submit button
Your profile time zone differs from the workspace owner’s #
If your profile is in a different time zone than the workspace owner, the submit button won’t appear due to how Clockify handles time zones.
- Go to the “Preferences” settings under your profile picture
- Change your time zone to match the owner’s
- Once aligned, submit the timesheet and revert to your native time zone (optional)
Clockify stores all time entries in the UTC time zone on the server. What you see in the web app is adjusted based on the time zone in your profile settings. This means:
- If your profile is set to a different timezone than the workspace owner, the start and end times of your entries may appear to fall outside the expected range for that timesheet period
- To prevent inaccurate approvals, the system disables the Submit button until everyone is aligned with the same time zone
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and include the following details:
- Your current time zone
- A screenshot of your timesheet view
- A screenshot of any warnings you might have received at the top of the timesheet page