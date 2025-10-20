# apps-manage-your-account

> Source: https://clockify.me/help/apps/manage-your-account

Manage your Marketplace account
This article provides an insight into the concept of the Marketplace account and the account management functionalities.
User account overview #
In your Marketplace profile, you can access your basic data and view a comprehensive list of installed add-ons. These add-ons are categorized based on the product and the workspace they were installed in.
General tab #
Each profile contains some general info in the General tab:
It’s accessible to all signed-in users, but with certain information is visible only to users with an admin role.
It includes:
- Profile photo: Taken from the first product account used to sign in to the Marketplace. You can modify it in the profile settings of your Clockify product account.
- Name: The name you registered your first product account with, also unchangeable from the Marketplace.
- Email: The email you registered your first product account with, also unchangeable from the Marketplace.
- Marketplace account button: Leads to the Manage accounts page.
- Log out: Click here to log out. It’ll redirect you to the Marketplace landing page.
If you are an admin and have at least one workspace with at least one installed add-on, you’ll see a list of installed add-ons with the details:
- Add-on name
- Date of update
- Date of installation: In case of reinstallation, the last date is shown
- Who installed
- Add-on status
- Date of deactivation (if there is any)
Add-ons listed here are sorted in the descending order based on their installation details. Unlisted add-ons are also visible in the list.
Please note that you can access unlisted add-ons directly from your Clockify profile, or through the direct link.
However, the access is limited to workspaces where the add-on was initially installed.
Add-on status #
Add-on status indicates the status of the add-on in the payment and installation process.
It can be:
- Deactivated: Add-on has been deactivated
- Installed: Add-on has been installed successfully
- Overdue: After the subscription runs out, the installed add-on is marked as Overdue
- Payment failed: Payment process failed and add-on cannot be used
- Uninstalled: Add-on is unistalled
Customer & Payment information tab #
Customer & payment information tab visible only to workspace admins that have installed paid add-on at one point in time
Invoices #
Invoices tab appears when invoices are available on Stripe.
It shows:
- Date: DD/MM/YY
- Status: Paid / Open
- Amount: Total invoice value (formatted by Clockify, up to 2 decimals)
- Product: Clockify / Pumble / Plaky
- Description: Type of transaction
- Download: Click to get the invoice in PDF format
Manage accounts page #
The Manage accounts page allows you to add or remove product accounts to or from the Marketplace account.
This can be useful if you, for example, want to access the Marketplace with more than one account, but don’t want to be signing in and out of the Marketplace and Clockify all the time (multiple times). This way you’ll have an overview of all the add-ons installed across your multiple accounts and products.
If you click Log in with Clockify and are already logged in to your Marketplace account, you’ll be automatically redirected to this (Manage accounts) page with a message confirming that the account has already been created.
If one of the products has both regional (or global) and subdomain accounts, they will be split into two accounts in the table. The Manage accounts table will display this as two separate accounts, each connected to a different URL.
Verify account #
If your account needs to be verified, you’ll be redirected to the Clockify login page where you’ll be prompted to verify your account.
Delete Marketplace account #
If you click Delete account, a new page with account deletion details appears requiring you to confirm the action.
Account deletion occurs automatically when all associated products are deleted, since there is no way to sign in without them.
If you delete a Clockify account, that account will be deleted from all connected workspaces.
After account is deleted:
- Installed add-ons are uninstalled
- Subscription is canceled for paid add-ons
Remove Marketplace account #
When considering removing an account, you need to check if you’re the only admin or owner of any workspace. Similar to deleting a Marketplace account, removing an account with admin privileges will result in the deletion of certain add-ons associated with the workspace.