# track-time-and-expenses-adding-time-manually

> Source: https://clockify.me/help/track-time-and-expenses/adding-time-manually

Add time manually
If you forgot to start the timer, or you prefer to fill in all your work hours in one go, use manual mode.
Manual mode is also useful when you want to add past activities/events (e.g. previous week’s day to your timesheet).
Manual mode lets you add time entries one by one, specify start and end times, and date.
- Enter manual mode by clicking the list icon in the upper right corner on the Time Tracker page
- Optionally, type what you’ve worked on in the What have you worked on? box
- Optionally, mark time as billable, select project/task, and add tags
- Set the start and end time, or add time by duration
- Change the date if needed, by clicking on the calendar icon and selecting the date
- Add the entry by clicking ADD
If you’re adding a time entry for a different date, it will be added to the appropriate day header (whether the date is in the past or the future).
You can also use keyboard shortcuts when navigating through the Time Tracker page. Use TAB to move through fields and press Enter when you select ADD to add a new entry.
Add time by duration #
Manual mode lets you add time entries by duration. Let’s say you’ve started working 2 hours ago, but you didn’t start the timer. To add past time:
- Switch to manual mode
- Click on the time (00:00:00)
- Type 2h (or 200 or 2:00)
- Click ADD to add the time entry
When you type 2h, the current time will be used as the start time and “the current time + 2h” as the end time.
You can input time in both clock and decimal notation. For example, to represent 2 hours and 45 minutes you worked, you can enter either “2.75” in decimal, or “2:45” in clock notation.
Duration format guide #
- If you type anything between 1 and 59, it will be interpreted as minutes (1 will become 1m)
- If you’re using decimal format, it will be interpreted as hours (1 will become 1h)
- If you type 60 or 99, it will be interpreted as 1h or 1h39m
- If you type 123 or 1234, it will be interpreted as 1h23m or 12h34m
- If you type 1:1 it will be interpreted as 1h1m (1:61 will become 2h01m)
- If you type 1:1:1, it will be interpreted as 1h1m1s
- If you type 1h, 30m, 1s, 1h30m1s, it will be interpreted as 1 hour, 30 minutes, 1 second, or 1 hour 30 minutes and 1 second (or any other combo)
- If you type 0.1, it will be interpreted as 6 minutes (0.2 will become 12m, 1.5 will become 1h30m, 7.2 will become 7h12min)
- If you type 1.0 or 1,0, it will be interpreted as 1 hour
- If you type :30, it will be interpreted as 30 minutes
- If you type .5 or .25, it will be interpreted as 30 minutes or 15 minutes
- If you add multiple time entries, end time of the previous entry will be the start time of the next one
Input format for start and end time #
When you input the start and end time the duration will be displayed in the decimal format set in the settings: Full (hh:mm:ss), Compact (h:mm), Decimal (h.hh).
Clockify also accepts alternative inputs:
- You can omit the colons (e.g. 0345 will become 03:45/3:45AM)
- You can also use dots instead of colons (e.g. 9.45 will become 9:45)
- You can type 1am/1 am, 1pm/1 pm and it will get converted to 01:00/1:00AM and 13:00/1:00PM, respectively
- If you type just one or two numbers, they will be treated as hours (e.g. 1 will become 01:00/01:00AM and 13 will become 13:00/1:00PM)
- If you type three numbers, the first number will become the hour and last two will become minutes (e.g. 130 will become 1:30/1:30AM)
You can control whether you want Clockify to show time in 12-hour or 24-hour format in your Profile settings.
Please note that, if the start and end time include an overnight period, there will be a superscript number next to the end time, showing how many additional days the time entry covers.
Add time manually while your timer is running #
While it’s not possible to manually input time while you have a current timer running, you can use the duplicate option of a previous entry.
This will create a new time entry exactly as the previous one and you can change the details of that entry to whatever you need.
Force Timer #
With the Force timer feature available in the Pro plan, the manual mode on the Time Tracker can be disabled.