# troubleshooting-cant-stop-the-timer

> Source: https://clockify.me/help/troubleshooting/cant-stop-the-timer

I can’t stop the timer
If you are having trouble stopping a running timer, it’s usually because something is missing or restricted.
Check if any required fields are missing #
If your workspace requires fields like a project, task, or a description, the timer won’t stop until you add that info.
- Open the Time Tracker page
- Look for fields marked with a red asterisk
- Enter the missing details
- Try stopping the timer again
Long-running timer #
If your timer has been running for a long time (e.g., overnight) and your workspace has the lock timesheets feature enabled, this can prevent you from stopping the running timer.
- Check the total duration of the time entry
- If the timer crosses into a locked day (e.g., longer than 10 hours), you won’t be able to stop it
- Ask your workspace admin to adjust or unlock the timesheet, or you can discard the timer
Device time is not synced #
If your device’s time isn’t synced correctly, it can prevent the timer from stopping.
Clockify stores time entries in UTC to keep data consistent across all users and locations. If your device time, browser settings, and actual time zone don’t match, Clockify might not be able to calculate the time duration correctly.
Example:
If you start a timer while your device is set to GMT+2 and later your system switches to GMT+0 (or is incorrect), Clockify will see the stop time as before the start time and prevent you from saving it.
- Visit time.is to check if your device time matches the real time
- If it’s off, update your device time settings to sync automatically with your time zone
- Try stopping the timer again
How to check and correct your time settings
On Windows:
- Click the Start menu and open Settings
- Go to Time & Language > Date & Time
- Toggle “Set time automatically” and “Set time zone automatically” to On
- If needed, manually select the correct time zone
- Restart your browser and refresh Clockify
On macOS:
- Open System Settings (or System Preferences on older versions)
- Go to General > Date & Time
- Enable Set time and date automatically
- Turn on Set time zone automatically using current location if available
- Restart your browser and refresh Clockify
Still not working?
- Refresh your browser
- Log out and log back in
- Try using a different browser or incognito mode
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and provide us with the following information:
- A screenshot of the issue from the Time Tracker page
- Any error messages you’re seeing on the Time Tracker page