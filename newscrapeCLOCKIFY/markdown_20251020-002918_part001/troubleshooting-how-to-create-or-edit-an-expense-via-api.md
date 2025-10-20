# troubleshooting-how-to-create-or-edit-an-expense-via-api

> Source: https://clockify.me/help/troubleshooting/how-to-create-or-edit-an-expense-via-api

How to create or edit an expense via API
1 min read
These instructions explain how to create or edit an expense using the Clockify API, which requires a specific formatting technique. Expenses are handled differently compared to other API requests in Clockify.
Steps to create/edit an expense via API #
- Log in to Postman: Ensure you are logged into your Postman account
- Create a POST (create expense) or PUT (edit expense) request:
- Set the request path to
/v1/workspaces/{workspaceId}/expenses
- Set the request path to
- Set headers:
- Add
X-Api-Key
for authentication - Set
Content-Type
tomultipart/form-data
- Add
- Body format:
- Choose
form-data
instead ofraw
for the body type - Enter the following keys and corresponding values (without quotes):
- KEY:
user_id
,date, project_id
,category_id
,notes
,amount
,billable
- VALUE: Enter the data values directly (no quotations around the values)
- KEY:
- Choose
- Send the request: After sending, check the status of the request
- If successful, you should see a
201 Created
response - The response will be displayed in JSON format
- If successful, you should see a
Was this article helpful?
Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me