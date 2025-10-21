# Create & manage invoices

> URL: https://clockify.me/help/projects/invoicing

In this article

* [Create invoices](#create-invoices)
* [Edit invoice](#edit-invoice)
* [Taxes](#taxes)
* [Filter invoices](#filter-invoices)
* [Sort by time entry or expense details](#sort-by-time-entry-or-expense-details)
* [Additional invoice settings](#additional-invoice-settings)
* [Set up translations](#set-up-translations)

# Create & manage invoices

12 min read

Create invoices for clients based on tracked time and mark entries as invoiced, so you don’t double bill clients.

Invoicing is a paid feature, which you can use if you [upgrade](https://clockify.me/pricing) your workspace to Standard, Pro, or Enterprise plan.

For step-by-step guidance on how to create and manage invoices in Clockify, watch the video and follow the instructions below.

User interface displayed in this video may not correspond to the latest version of the app.

Invoicing needs to be enabled in the **Workspace settings**.

## Create invoices [#](#create-invoices)

To create invoices:

1. Go to the **Invoices** page
2. Click **Create invoice**
3. Choose client
4. Change currency, invoice number, and issue/due dates (if needed)
5. Click **Create**

![](https://clockify.me/help/wp-content/uploads/2024/02/Screenshot-2024-02-09-at-09.31.35.png)

After you’ve done that, you can also make some additional changes like:

* Manually add items to the invoice
* Import your tracked time and expenses
* Download the invoice
* [Set taxation mode](https://clockify.me/help/projects/invoicing#set-taxation-mode-on-individual-invoices)

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-02-20-at-09.26.28-1024x457.png)

There are also some actions you can do such as to duplicate the existing invoice and quickly create a new one.

1. Choose the invoice you’d like to duplicate
2. Click on the three dots menu
3. Choose the **Duplicate** option from the dropdown

![](https://clockify.me/help/wp-content/uploads/2024/02/Screenshot-2024-02-09-at-09.34.08.png)

This newly-created invoice contains the same information as the original one. This information can be changed and edited according to your needs. Any imported time entries won’t carry over their dependency.

**Bill from**, **name**, **address** and logo are taken from your **Workspace settings**, and **Bill to address** is taken from the client.

 To edit client address:

1. Go to the **Clients** page
2. Choose client
3. Click the edit icon and edit their address

Expand your contact list in the settings on the **Invoices** page. Once you add more contacts, they’ll appear in the **Bill from** the dropdown on any invoice.

Admins can access the Invoices page. You can allow specific members to also see and manage in workspace settings under the Who can manage invoices section.

### Set up recurring invoices [#](#set-up-recurring-invoices)

COMING SOON

Save time and minimize errors by automating recurring invoices that repeat at custom intervals, weekly or monthly.

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-04-08-at-14.18.16.png)

## Edit invoice [#](#edit-invoice)

To edit an invoice:

1. Go to the invoice you’d like to edit
2. Choose an action from the **Actions** dropdown in the upper right corner
3. Choose one of the following actions:
   * See all your invoices
   * Filter invoices by status
   * Mark invoices as **Sent**, **Paid**, **Void**
   * Edit, delete, change status of an invoice
   * Download expenses

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-07-18-at-12.55.36-1024x595.png)

### Record payment [#](#record-payment)

Record payment option saves the invoice payment.

To record invoice payment:

1. Choose the **Record payment** option
2. **Record payment** screen appears
   * **Date**: Enter today’s date
   * **Amount**: Enter unpaid invoice amount you’d like to mark as **Paid**
   * Optionally change **Date**, **Amount** or add a **Note**

Click **Save** to complete the action.

As a result, invoice is marked as:

* **Paid** (you entered full amount)
* **Partially paid**: (you entered amount smaller than invoice amount)

Amount is displayed in currency assigned to the client.

#### Payments window [#](#payments-window)

When an invoice is marked as **Paid**, you’ll see the **Payments** option in the three-dot menu. This will open a list of all recorded payments for that invoice.

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-01-28-at-11.32.37-1024x231.png)

The **Payments** window includes the following details:

* **Date**: The payment date
* **Author**: The person who made the payment
* **Amount**: The total amount paid
* **Note**: An optional field where you can add a note

#### Invoice status [#](#invoice-status)

* Invoice with **Partially paid**, **Fully paid** and **Void** status cannot be edited; In order to be edited, paid invoices need to be marked as either **Unsent** or **Sent**
* If invoice status is **Partially paid**, you can see all previously invoiced payments
* If record payment amount is negative number or zero, invoice can be immediately marked as **Paid**
* If due date for sent invoice passes, invoice gets an **Overdue** status
* If status is changed to **Unsent**, all previously processed payments are deleted

All other invoices need to be processed through the **Record payment** option.

### Manually configure invoices [#](#manually-configure-invoices)

Clockify allows you to manually mark time entries and expenses as invoiced/uninvoiced. This way you have complete control over the invoicing workflow, accurate time and expense tracking without duplicated invoices errors.

To manually mark time as invoiced:

1. Go to the **Detailed report**
2. Choose all time entries you need via **Bulk edit**
3. Click on **Mark as invoiced** (next to Bulk edit in table header)

![](https://clockify.me/help/wp-content/uploads/2024/02/Screenshot-2024-02-09-at-09.47.48-1024x503.png)

Invoiced time entries have a green **Invoiced** tag next to them in the **Detailed report**.

When you hover over the **Invoiced** tag, you’ll see the client and the invoice ID under which the time entry was invoiced (unless it was manually marked as invoiced).

By default, each new invoiceID is automatically assigned a unique number in sequence, such as invoice1, invoice2, invoice3, and so on, thanks to the auto-increment feature.

To mark time as uninvoiced:

1. Choose only invoiced time entries
2. Click **Mark as uninvoiced**

![](https://clockify.me/help/wp-content/uploads/2024/02/Screenshot-2024-02-09-at-09.49.44-1024x501.png)

### Conversion from clock to decimal format [#](#conversion-from-clock-to-decimal-format)

Total amount between reports and invoices may slightly differ.

Invoices round time on two decimals, while reports take more decimals into account.

For example:  
*You have a time entry whose duration is 20min, or 0.3333333h when converted to decimal format. When a report multiplies it with hourly rate of $100, the result in the report is $33.33. But when that entry is imported into an invoice, the invoice imports time rounded to two decimals (0.33h), which when multiplied with $100 equals $33.00.*

Grouping option may also result in different total amounts.

For example:  
*You have three entries on some project, each 20min. If you import time one by one with the Group hours: Detailed option, the invoice will make three line items of 0.33 and total amount will be $99.00 (3 x 0.33h x $100). But if you choose Group hours: Project option, they will be summed up and rounded using more decimals (like in the reports), resulting in $100.00 invoice.*

To avoid discrepancy due to the decimal rounding, round time up, down, or to nearest number 6/12/15/30 minutes (i.e. any number divisible by six).

## Taxes [#](#taxes)

**Tax** fields in an invoice form shows the amount of tax added to the total price of a product or a service. Tax can either be a general amount added to the total, or broken down by the item, depending on the tax system used. Clockify uses item-based tax system.

### Item-based taxes [#](#item-based-taxes)

Item-based taxes are used to apply taxes individually to each item on an invoice. This way you can have a better control over your taxes, making sure that taxes are applied only to relevant items.

This feature is available to users on [Standard](https://clockify.me/help/administration/subscription-plans#standard) and higher subscription plans and on [Free trial](https://clockify.me/help/administration/free-trial).

In order to use it, the Invoicing feature needs to be enabled in the **[Workspace settings](https://clockify.me/help/track-time-and-expenses/workspaces#workspace-settings)**:

1. Navigate to the workspace name at the top left corner of the page
2. Open the three-dot menu and choose **Workspace settings**
3. Navigate to the **Invoicing** section in the **General** settings and toggle the switch to enable it

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfTgQRth161qt7YFj7ONKUfZfgJD7DUHBHbGxR1P7C4t434aRR2hUrKmTZvI5HGWhrAcO19phzm7GmfWaB3TE_K37ifXRMEVxFB0gNXea67rjROpCe5SZWXtiwI8Oz-gPDcgMgvUyrhZCp56TA5TrEq3V0?key=om-QeMoD2lNvGTlhUn5IiA)

User permissions for this feature depend on the settings in the Permissions tab, in the Workspace settings.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdaH5AgGxun999Ns1wvzxDsikVdA-pKDC6cJwi0H0HolO2ZE6NZmZtc3ltt6-k00aTV_48xiI_IvkzDeGNN4-dxordtZ5PVtyOKWJpyKbRF6VQAdEuZn0rM5a9Fxvd9LzN_T7js5OIsThmg0B2NHaKx1mRO?key=om-QeMoD2lNvGTlhUn5IiA)

#### How item-based taxes work [#](#how-item-based-taxes-work)

 When you create a new invoice, you will see two columns after the **AMOUNT** column:

* **TAX** (if only one tax is enabled)
* **TAX 2** (if a second tax is enabled in the settings)

Each item on the invoice has checkboxes next to the **TAX** and **TAX 2** columns. By default, these checkboxes are checked (blue with a white tick), indicating that the taxes are applied. Unchecking them means that taxes will **not** be applied to that particular item.

Taxes are calculated in the following way:

* **TAX**: This is calculated based on the percentage defined in the **Invoice Settings**
* **TAX 2**: If enabled, this is also calculated as a percentage of the item amount

#### Taxation mode [#](#taxation-mode)

Taxation mode can be:

* **Simple**: Both taxes are applied to the total amount of the item
  + E.g.: For an item priced at $100, with **Tax 1** at 10% and **Tax 2** at 10%, the calculated taxes will be $10 for each, making the total $120.
* **Compound**: The second tax is applied on the taxed amount, not the item amount.
  + E.g.: For an item priced at $100, with **Tax 1** at 10% and **Tax 2** at 10%, **Tax 1** is $10, and **Tax 2** is calculated on the taxed amount, resulting in $11 for **Tax 2**, making the total $121.

The **checkboxes** for **TAX** and **TAX 2** are remembered for each item on the invoice, meaning that the selected state is retained until the invoice is manually edited or changes are made to the tax settings. If you change the tax percentage during invoice creation, the totals will update automatically to reflect the new tax rates.  
If you switch from **Simple** to **Compound** or vice versa, all **Unsent invoices** will automatically update to match the new taxation settings.

For example:

* **Simple to Compound mode**: The **Apply tax** checkbox will appear next to each item
* **Compound to simple mode**: The **Tax** and **Tax 2** checkboxes will reappear

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-07-18-at-12.57.34-1024x608.png)

If you remove one of the taxes from an invoice, then selected taxation mode will also be removed.   
If you add a previously removed tax, the system will remember the last selected taxation mode for that invoice.

#### Set taxation mode on individual invoices [#](#set-taxation-mode-on-individual-invoices)

If you’re using two taxes (**TAX** and **TAX 2**) you can set a default taxation mode in the **Invoice settings** that will be applied to all new invoices. However, you can override these default settings for individual invoices when creating or editing.

To do that:

1. Open the invoice you’re working on
2. Scroll down to the **Taxation mode** section
3. Choose whether **Simple** or **Compound** taxation mode should be applied to that specific invoice

![](https://clockify.me/help/wp-content/uploads/2020/11/Screenshot-2025-07-18-at-13.06.13-1024x328.png)

Taxation mode for a new invoice will not affect any invoices that are already **Partially paid**, **Paid** or **Void**.

## Filter invoices [#](#filter-invoices)

You can filter invoices by:

* Status
* Issue date
* Client
* ID
* Bill from contact
* Amount

To filter invoices:

1. Go to the **Invoices** page
2. Choose filter criteria at the top of the **Invoices** page:
   * Date range
   * Click **Apply filter**
   * Client
   * Status
   * Amount
   * Balance
   * Invoice ID

![](https://clockify.me/help/wp-content/uploads/2024/03/Screenshot-2024-03-21-at-13.32.49-1024x481.png)

All invoices will be filtered out according to the selected criteria.

## Sort by time entry or expense details [#](#sort-by-time-entry-or-expense-details)

When you create a new invoice or edit the existing one and import time and expenses, you can choose to display them according to the details in the **Detailed view**.

To display entries and expenses in **Detailed view**:

1. Choose the invoice on the **Invoices** page
2. Click on **Import time and expenses** at the bottom of the page
3. Choose **Detailed** in **Display time** dropdown

In **Show in invoice** label choose the tag by checking the box and rearrange them by drag & drop. The checkbox you chose will appear in the Item’s description.

![](https://lh7-us.googleusercontent.com/V5HVjRqgk2AJkwWRrdGRIa6RNyFN-FZVYv5-KyfukM_8J0cgYNwEo5FjvzKZdvWhvVA0EM_lHhzzjMVESo6UslQ9qW52mMZZdHf1HxNiCfkTGGfzn9Lzpy5Cink7S_MH3FptaDimZlpdHg4KBjAqTr0)

Same behavior is applied for **Expense details** and **Time entry details**.

When different billing rates are applied, entries are always displayed in multiple lines, overriding the single-line option.

## Additional invoice settings [#](#additional-invoice-settings)

You can get invoices in another language or name things differently (e.g. change label from Tax to VAT):

1. Go to the **Invoices** page
2. Click on the **cog icon** (settings) next to the **Create invoice** button
3. In the **Defaults tab**, edit the content you’d like to be displayed in each label

After the changes you’ve made, each PDF you generate will display the new labels.  
When you create a new invoice, it can inherit some predefined subject, note, issue date, and tax.

To set defaults:

1. Go to **Invoices** page
2. Click on the **cog icon** (Settings) on the **Invoices** pages
3. Make the necessary changes in the **Defaults** tab

Customize invoices exported in **PDF** from the **Appearance** tab in the **Invoice Settings**. Here, you have the option to hide **Quantity** and **Unit Price** columns, as well as toggle text direction from left-to-right or right-to-left.   
Enable detailed invoicing by including TAX and TAX2 columns in your PDF exports simply by checking the provided boxes.

### Existing invoices [#](#existing-invoices)

When the user clicks on the Invoices tab and enters any of the invoices, after the **Amount** column, there should be two columns. TAX and TAX 2 depending on whether you applied one or two taxes on your invoices.

Paid and partially paid invoices cannot be edited and the checkboxes are disabled, as well.

### Download invoices in PDF [#](#download-invoices-in-pdf)

You can choose which columns should be visible in the downloaded PDF file. You can customize the PDF in the **Invoice settings** > **Appearance tab** and choose if you’d like to include TAX and TAX 2.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdc925DY-qBKMoDVDK0bITPk5NDTo62Qruq5b9V6kax6ybRT6aBcSIzQzu59BCXP9rHsH1kA1Y30LfnOa1dB6XecPOd_utFrw6QYc6k-2J1yolzqS4BwlBPTeKVLpPELEY9XU7ksWV_IIqdrMdoH6GQt9c?key=om-QeMoD2lNvGTlhUn5IiA)

Depending on which items you checked, those columns will be displayed in the PDF file.

TAX and TAX 2 are system names which can be changed for the download file in the Invoices, Translation tab, where TAX and TAX 2 are input fields.

## Set up translations [#](#set-up-translations)

With translations, you can customize labels on your invoices, from item types to total amounts due.

Translations will appear on the PDF and printed versions of all your invoices.

1. Click on the **cog icon** (Settings) next to the **Create invoice** button on the **Invoices** page
2. Choose the **Translations** tab
3. Locate the field labeled **Item type** and enter your translation
4. Repeat step 3 for each relevant field
5. Save your translations

![](https://lh7-us.googleusercontent.com/P8PqVwon9aS-0klbEFs455oxn_ch74YGP_RkZ9r5lO_Mr4c8v76CPk6Pqf7c8M_EKMHUARXXfAKpdJhELoM4SUm8G_2IafKYeREBeEM5DQU72eMmAiOMPGLMMIgwr_KsxvBk3o9Kqrs3ZhX7aSBz-lg)

If you delete a value in the label field, that label won’t appear in the PDF version of the invoice.

### Related articles [#](#related-articles)

* [Invoice tracked time & expenses](https://clockify.me/help/projects/invoicing-tracked-time-expenses)
* [Send invoice emails](https://clockify.me/help/projects/sending-invoice-emails)
* [Export invoices](https://clockify.me/help/projects/export-invoices)

### Was this article helpful?

Submit
Cancel

Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me