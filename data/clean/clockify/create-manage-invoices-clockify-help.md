# Create & manage invoices - Clockify Help

**Source:** https://clockify.me/help/projects/invoicing

Projects
Clockify Help Center
Projects
Create & manage invoices
In this article
Create invoices
Edit invoice
Taxes
Filter invoices
Sort by time entry or expense details
Additional invoice settings
Set up translations
Create & manage invoices
12 min read
Create invoices for clients based on tracked time and mark entries as invoiced, so you don’t double bill clients.
Invoicing is a paid feature, which you can use if you
upgrade
your workspace to Standard, Pro, or Enterprise plan.
For step-by-step guidance on how to create and manage invoices in Clockify, watch the video and follow the instructions below.
User interface displayed in this video may not correspond to the latest version of the app.
Invoicing needs to be enabled in the
Workspace settings
.
Create invoices
#
To create invoices:
Go to the
Invoices
page
Click
Create invoice
Choose client
Change currency, invoice number, and issue/due dates (if needed)
Click
Create
After you’ve done that, you can also make some additional changes like:
Manually add items to the invoice
Import your tracked time and expenses
Download the invoice
Set taxation mode
There are also some actions you can do such as to duplicate the existing invoice and quickly create a new one.
Choose the invoice you’d like to duplicate
Click on the three dots menu
Choose the
Duplicate
option from the dropdown
This newly-created invoice contains the same information as the original one. This information can be changed and edited according to your needs. Any imported time entries won’t carry over their dependency.
Bill from
,
name
,
address
and logo are taken from your
Workspace settings
, and
Bill to address
is taken from the client.
To edit client address:
Go to the
Clients
page
Choose client
Click the edit icon and edit their address
Expand your contact list in the settings on the
Invoices
page. Once you add more contacts, they’ll appear in the
Bill from
the dropdown on any invoice.
Admins can access the Invoices page. You can allow specific members to also see and manage in workspace settings under the Who can manage invoices section.
Set up recurring invoices
#
COMING SOON
Save time and minimize errors by automating recurring invoices that repeat at custom intervals, weekly or monthly.
Edit invoice
#
To edit an invoice:
Go to the invoice you’d like to edit
Choose an action from the
Actions
dropdown in the upper right corner
Choose one of the following actions:
See all your invoices
Filter invoices by status
Mark invoices as
Sent
,
Paid
,
Void
Edit, delete, change status of an invoice
Download expenses
Record payment
#
Record payment option saves the invoice payment.
To record invoice payment:
Choose the
Record payment
option
Record payment
screen appears
Date
: Enter today’s date
Amount
: Enter unpaid invoice amount you’d like to mark as
Paid
Optionally change
Date
,
Amount
or add a
Note
Click
Save
to complete the action.
As a result, invoice is marked as:
Paid
(you entered full amount)
Partially paid
: (you entered amount smaller than invoice amount)
Amount is displayed in currency assigned to the client.
Payments window
#
When an invoice is marked as
Paid
, you’ll see the
Payments
option in the three-dot menu. This will open a list of all recorded payments for that invoice.
The
Payments
window includes the following details:
Date
: The payment date
Author
: The person who made the payment
Amount
: The total amount paid
Note
: An optional field where you can add a note
Invoice status
#
Invoice with
Partially paid
,
Fully paid
and
Void
status cannot be edited; In order to be edited, paid invoices need to be marked as either
Unsent
or
Sent
If invoice status is
Partially paid
, you can see all previously invoiced payments
If record payment amount is negative number or zero, invoice can be immediately marked as
Paid
If due date for sent invoice passes, invoice gets an
Overdue
status
If status is changed to
Unsent
, all previously processed payments are deleted
All other invoices need to be processed through the
Record payment
option.
Manually configure invoices
#
Clockify allows you to manually mark time entries and expenses as invoiced/uninvoiced. This way you have complete control over the invoicing workflow, accurate time and expense tracking without duplicated invoices errors.
To manually mark time as invoiced:
Go to the
Detailed report
Choose all time entries you need via
Bulk edit
Click on
Mark as invoiced
(next to Bulk edit in table header)
Invoiced time entries have a green
Invoiced
tag next to them in the
Detailed report
.
When you hover over the
Invoiced
tag, you’ll see the client and the invoice ID under which the time entry was invoiced (unless it was manually marked as invoiced).
By default, each new invoiceID is automatically assigned a unique number in sequence, such as invoice1, invoice2, invoice3, and so on, thanks to the auto-increment feature.
To mark time as uninvoiced:
Choose only invoiced time entries
Click
Mark as uninvoiced
Conversion from clock to decimal format
#
Total amount between reports and invoices may slightly differ.
Invoices round time on two decimals, while reports take more decimals into account.
For example:
You have a time entry whose duration is 20min, or 0.3333333h when converted to decimal format. When a report multiplies it with hourly rate of $100, the result in the report is $33.33. But when that entry is imported into an invoice, the invoice imports time rounded to two decimals (0.33h), which when multiplied with $100 equals $33.00.
Grouping option may also result in different total amounts.
For example:
You have three entries on some project, each 20min. If you import time one by one with the Group hours: Detailed option, the invoice will make three line items of 0.33 and total amount will be $99.00 (3 x 0.33h x $100). But if you choose Group hours: Project option, they will be summed up and rounded using more decimals (like in the reports), resulting in $100.00 invoice.
To avoid discrepancy due to the decimal rounding, round time up, down, or to nearest number 6/12/15/30 minutes (i.e. any number divisible by six).
Taxes
#
Tax
fields in an invoice form shows the amount of tax added to the total price of a product or a service. Tax can either be a general amount added to the total, or broken down by the item, depending on the tax system used. Clockify uses item-based tax system.
Item-based taxes
#
Item-based taxes are used to apply taxes individually to each item on an invoice. This way you can have a better control over your taxes, making sure that taxes are applied only to relevant items.
This feature is available to users on
Standard
and higher subscription plans and on
Free trial
.
In order to use it, the Invoicing feature needs to be enabled in the
Workspace settings
:
Navigate to the workspace name at the top left corner of the page
Open the three-dot menu and choose
Workspace settings
Navigate to the
Invoicing
section in the
General
settings and toggle the switch to enable it
User permissions for this feature depend on the settings in the Permissions tab, in the Workspace settings.
How item-based taxes work
#
When you create a new invoice, you will see two columns after the
AMOUNT
column:
TAX
(if only one tax is enabled)
TAX 2
(if a second tax is enabled in the settings)
Each item on the invoice has checkboxes next to the
TAX
and
TAX 2
columns. By default, these checkboxes are checked (blue with a white tick), indicating that the taxes are applied. Unchecking them means that taxes will
not
be applied to that particular item.
Taxes are calculated in the following way:
TAX
: This is calculated based on the percentage defined in the
Invoice Settings
TAX 2
: If enabled, this is also calculated as a percentage of the item amount
Taxation mode
#
Taxation mode can be:
Simple
: Both taxes are applied to the total amount of the item
E.g.: For an item priced at $100, with
Tax 1
at 10% and
Tax 2
at 10%, the calculated taxes will be $10 for each, making the total $120.
Compound
: The second tax is applied on the taxed amount, not the item amount.
E.g.: For an item priced at $100, with
Tax 1
at 10% and
Tax 2
at 10%,
Tax 1
is $10, and
Tax 2
is calculated on the taxed amount, resulting in $11 for
Tax 2
, making the total $121.
The
checkboxes
for
TAX
and
TAX 2
are remembered for each item on the invoice, meaning that the selected state is retained until the invoice is manually edited or changes are made to the tax settings. If you change the tax percentage during invoice creation, the totals will update automatically to reflect the new tax rates.
If you switch from
Simple
to
Compound
or vice versa, all
Unsent invoices
will automatically update to match the new taxation settings.
For example:
Simple to Compound mode
: The
Apply tax
checkbox will appear next to each item
Compound to simple mode
: The
Tax
and
Tax 2
checkboxes will reappear
If you remove one of the taxes from an invoice, then selected taxation mode will also be removed.
If you add a previously removed tax, the system will remember the last selected taxation mode for that invoice.
Set taxation mode on individual invoices
#
If you’re using two taxes (
TAX
and
TAX 2
) you can set a default taxation mode in the
Invoice settings
that will be applied to all new invoices. However, you can override these default settings for individual invoices when creating or editing.
To do that:
Open the invoice you’re working on
Scroll down to the
Taxation mode
section
Choose whether
Simple
or
Compound
taxation mode should be applied to that specific invoice
Taxation mode for a new invoice will not affect any invoices that are already
Partially paid
,
Paid
or
Void
.
Filter invoices
#
You can filter invoices by:
Status
Issue date
Client
ID
Bill from contact
Amount
To filter invoices:
Go to the
Invoices
page
Choose filter criteria at the top of the
Invoices
page:
Date range
Click
Apply filter
Client
Status
Amount
Balance
Invoice ID
All invoices will be filtered out according to the selected criteria.
Sort by time entry or expense details
#
When you create a new invoice or edit the existing one and import time and expenses, you can choose to display them according to the details in the
Detailed view
.
To display entries and expenses in
Detailed view
:
Choose the invoice on the
Invoices
page
Click on
Import time and expenses
at the bottom of the page
Choose
Detailed
in
Display time
dropdown
In
Show in invoice
label choose the tag by checking the box and rearrange them by drag & drop. The checkbox you chose will appear in the Item’s description.
Same behavior is applied for
Expense details
and
Time entry details
.
When different billing rates are applied, entries are always displayed in multiple lines, overriding the single-line option.
Additional invoice settings
#
You can get invoices in another language or name things differently (e.g. change label from Tax to VAT):
Go to the
Invoices
page
Click on the
cog icon
(settings) next to the
Create invoice
button
In the
Defaults tab
, edit the content you’d like to be displayed in each label
After the changes you’ve made, each PDF you generate will display the new labels.
When you create a new invoice, it can inherit some predefined subject, note, issue date, and tax.
To set defaults:
Go to
Invoices
page
Click on the
cog icon
(Settings) on the
Invoices
pages
Make the necessary changes in the
Defaults
tab
Customize invoices exported in
PDF
from the
Appearance
tab in the
Invoice Settings
. Here, you have the option to hide
Quantity
and
Unit Price
columns, as well as toggle text direction from left-to-right or right-to-left.
Enable detailed invoicing by including TAX and TAX2 columns in your PDF exports simply by checking the provided boxes.
Existing invoices
#
When the user clicks on the Invoices tab and enters any of the invoices, after the
Amount
column, there should be two columns. TAX and TAX 2 depending on whether you applied one or two taxes on your invoices.
Paid and partially paid invoices cannot be edited and the checkboxes are disabled, as well.
Download invoices in PDF
#
You can choose which columns should be visible in the downloaded PDF file. You can customize the PDF in the
Invoice settings
>
Appearance tab
and choose if you’d like to include TAX and TAX 2.
Depending on which items you checked, those columns will be displayed in the PDF file.
TAX and TAX 2 are system names which can be changed for the download file in the Invoices, Translation tab, where TAX and TAX 2 are input fields.
Set up translations
#
With translations, you can customize labels on your invoices, from item types to total amounts due.
Translations will appear on the PDF and printed versions of all your invoices.
Click on the
cog icon
(Settings) next to the
Create invoice
button on the
Invoices
page
Choose the
Translations
tab
Locate the field labeled
Item type
and enter your translation
Repeat step 3 for each relevant field
Save your translations
If you delete a value in the label field, that label won’t appear in the PDF version of the invoice.
Related articles
#
Invoice tracked time & expenses
Send invoice emails
Export invoices
Was this article helpful?
Submit
Cancel
Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me
In this article
Create invoices
Edit invoice
Taxes
Filter invoices
Sort by time entry or expense details
Additional invoice settings
Set up translations