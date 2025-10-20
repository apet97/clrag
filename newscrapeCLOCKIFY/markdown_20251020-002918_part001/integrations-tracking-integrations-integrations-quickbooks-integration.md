# integrations-tracking-integrations-integrations-quickbooks-integration

> Source: https://clockify.me/help/integrations/tracking-integrations-integrations/quickbooks-integration

QuickBooks
Connect Clockify to your QuickBooks Online account and send time entries.
QuickBooks integration is a paid feature, which you can enable by upgrading your workspace to Clockify’s Standard, Pro, or Enterprise plan and QuickBooks’ Essentials, Plus, or Advanced plan.
Integration supports QuickBooks Online (Essentials or Plus plan). Doesn’t work with QuickBooks Desktop or QuickBooks Online Simple Start plan.
If you have Payroll feature enabled in QuickBooks, Clockify integration won’t work due to system’s capabilities.
Connect QuickBooks Online #
- Log in to your Clockify account
- Go to the three dots menu next to the workspace name
- Choose Workspace settings, then Integrations tab
- Expand QuickBooks section and click Connect to QuickBooks
- Authorize Clockify to access QuickBooks (you’ll need to be logged in to QuickBooks)
- Sync Clockify with QuickBooks
- Create missing users from Clockify and missing customers from QuickBooks
Before connecting to QuickBooks, make sure you have invited all users in Clockify, they have accepted the invite, and their names in Clockify (in Profile settings) and QuickBooks (their display name) are the same.
If you don’t have any projects in Clockify, everything will be pulled from QuickBooks so you don’t have to create anything manually.
If you add new user in Clockify, or new customer in QuickBooks, you’ll have to perform the sync again manually in the Integrations tabs before trying to send time to QuickBooks (Clockify won’t make any changes to your QuickBooks account unless you do it explicitly).
Please note that if you can’t sync certain time entries, you should check the settings on the QuickBooks side and whether Close the Books option is turned on for that year.
If you want to connect just one or several specific projects (e.g. to test the integration):
- Create a project with the same name as the customer (or project) in QuickBooks
- Create employee(s) in QuickBooks with same name as they have in Clockify
- Connect Clockify with QuickBooks
- After you’ve connected, DON’T create missing users and project (at this point, users and projects between Clockify and QuickBooks with the same name are connected to each other)
- Go to Detailed report, filter the report by the project/user you need, and send to QuickBooks
Set up Clockify for the first time #
- Invite team members to track time
- Make sure their names in Clockify and QuickBooks are the same
- Connect QuickBooks with Clockify
- Sync users and customers (this will create a project in Clockify for each QuickBooks project/customer)
- Track time on projects in Clockify
- Send tracked time to QuickBooks using Detailed report
Data mapping #
- User Name in Clockify and Employee Display Name in QuickBooks have to be identical in order to sync
- If user doesn’t exist in QuickBooks as an employee, you’ll perform sync in Settings > Integrations > QuickBooks
- Project Name in Clockify and Customer (or Project) Name in QuickBooks have to be identical in order to sync
- If you have parent customers in QuickBooks, Sub-customer in QuickBooks will be treated as Project in Clockify and its Parent in QuickBooks will be treated as Client in Clockify
- If a project doesn’t exist in QuickBooks as a customer (or project), you’ll first have to create it manually in QuickBooks using the exact same name as in Clockify, and perform sync in Settings > Integrations > QuickBooks
Also, keep in mind that QuickBooks has a robust structure with the hierarchy going up to four levels in depth:
- QuickBooks Customer ———> Clockify Client
- QuickBooks Sub-customer 1————> Clockify Client and Project (same name)
- QuickBooks Sub-customer 2 ———–> Clockify Client and Project (same name)
- QuickBooks Sub-customer 3 ————> Clockify Project
- QuickBooks Sub-customer 2 ———–> Clockify Client and Project (same name)
- QuickBooks Sub-customer 1————> Clockify Client and Project (same name)
This means that you can have customers that are both, a Parent customer and a Child customer (Sub-customer) at the same time (e.g. Sub-customer 2). In that case, when mapping it into Clockify, it will be mapped both, as a Client (since it’s a Parent of Sub-customer 3) and a Project (since it’s a Child of Sub-customer 1) with the same name.
QuickBooks also has a Project in their system. Depending on its position in the hierarchy, QuickBooks Project can be mapped either as Project or Client in Clockify as presented in the scheme above.
Send time to QuickBooks #
Once you’ve connected Clockify and QuickBooks, and synced users and customers/projects, you’ll see the QuickBooks button in the Detailed report.
- Go to the Detailed report
- Click QuickBooks button to see all time entries that haven’t been sent to QuickBooks
- Review if you wish to send all the data you see and apply filters if necessary
- Click Send to QuickBooks
Clockify sends the following information to QuickBooks:
- User
- Description
- Project
- Date
- Duration
- Billable status
- Billable rate
Once all the entries have been sent successfully, the system will mark them as sent. To see time entries that have been sent, click on the QuickBooks dropdown (next to Showing not sent entries), and choose Show sent entries.
Once an entry has been sent, it can’t be sent again. If you make changes to an entry, the change won’t be reflected in QuickBooks (meaning you’ll have to manually update time in QuickBooks too). To avoid this, it’s best to send only approved time to QuickBooks.
Notes
- It’s not possible to send billable entry without a project to QuickBooks
- If you turn rounding ON, Clockify will send rounded values
- Only Admins can send time to QuickBooks
- Individual time entries longer than 23h55m won’t be sent
- Clockify sends user’s name, date, project (i.e. customer in QB), billable status, hourly rate (if billable), duration, description
- Clockify also sends time entries of inactive and deleted users that were previously synced
Disconnect QuickBooks Online #
To disconnect your QuickBooks account:
- Log in to your Clockify account
- Go to the three dots menu next to the workspace name
- Choose Workspace settings, then Integrations tab
- Expand QuickBooks section and click Disconnect
- Confirm the action
Once you’ve disconnected QuickBooks, you’ll no longer see the QuickBooks button in Detailed report and Clockify won’t have access to your QuickBooks account.
You can reconnect to QuickBooks on the same page by clicking Connect to QuickBooks.