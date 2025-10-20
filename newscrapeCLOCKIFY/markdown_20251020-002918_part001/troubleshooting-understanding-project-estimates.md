# troubleshooting-understanding-project-estimates

> Source: https://clockify.me/help/troubleshooting/understanding-project-estimates

Understanding Project Estimates, Budgets, and Alerts
Clockify gives you multiple ways to track progress and stay informed through time estimates, budget estimates, and alerts. These features work in specific ways, and here’s a complete breakdown.
Estimate progress bars can exceed 100% #
When your tracked time or budget goes beyond the estimate, Clockify does not stop tracking. Instead, the project progress bar will go past 100% to reflect overage.
- 125% = 25% over the estimate
- This behavior is intentional and helps you measure how much you’ve exceeded
Recurring budgets reset automatically #
If you’ve set a weekly, monthly, or yearly recurring estimate, the budget will reset automatically at the end of each cycle based on the project’s start date.
What this means:
- Budgets don’t disappear; they just start fresh for the new period
- Project status only shows progress for the current cycle
How to preserve historical data
Before the reset date:
- Go to the Projects page
- Click Export (CSV or Excel)
- The export includes tracked time, budget, estimate, overage, progress, and more
This serves as a backup or a reference if you want to compare performance across periods.
Alerts may not trigger if not configured at that threshold #
Estimate alerts are only sent for thresholds that are explicitly defined.
Example:
If you set an alert only at 80% and not at 100%, you won’t receive anything when the estimate is fully reached.
What to do:
Set alerts at all relevant thresholds (e.g., 50%, 80%, 100%) under workspace settings -> Alerts.
Alerts are not retroactive #
If you create or edit an alert rule after a threshold is already passed, Clockify will not trigger the alert retroactively.
Clockify doesn’t block tracking beyond estimates #
Estimates are for informational purposes only. Clockify will not automatically prevent time tracking on those projects once an estimate or a budget is used up.
What you can do instead:
- Set up alerts to notify when the estimate is near or exceeded
- Use the Project status page to view the current status
- Create clear internal guidelines for stopping work manually
Optional control method:
Once the project reaches its estimate or a budget limit, an Admin or a Project Manager can:
- Go to the Projects page
- Click on the project
- Select Archive
This will prevent team members from tracking additional time on that project, effectively enforcing a soft stop.
Time estimate vs. Budget estimate #
Clockify allows you to track a project’s progress using two types of estimates: time estimates and budget estimates.
- A time estimate refers to the number of hours you expect to spend on a project. It’s based purely on tracked time entries and is ideal when you’re managing internal workload, capacity, or effort.
- A budget estimate, on the other hand, refers to the monetary value you expect to bill for a project. It depends on having hourly rates set up, either at the project or task level.
Task-level estimates also support alerts #
You can assign estimates and alerts to tasks, not just full projects.
You can notify:
- Task assignees
- Project Manager
- Workspace admin
Only one role can be selected per alert rule, but you can create multiple rules to notify several roles.
Estimate alerts are only sent once per threshold #
You’ll receive one alert per threshold (e.g., 80%, 100%). If the progress jumps over multiple thresholds at once (e.g., from 75% to 95%), only the highest one will trigger.
An alert for a threshold will only trigger again if the project drops below that value and then crosses it again.