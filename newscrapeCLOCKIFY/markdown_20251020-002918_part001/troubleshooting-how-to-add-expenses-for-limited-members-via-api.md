# troubleshooting-how-to-add-expenses-for-limited-members-via-api

> Source: https://clockify.me/help/troubleshooting/how-to-add-expenses-for-limited-members-via-api

How to add expenses for Limited members via API
This article will guide you through the process of adding expenses for Limited members using the Clockify API.
Add expenses for Limited members #
- Get user IDs of Limited members:
- Since the
GET /workspaces/{workspaceId}/users
endpoint does not provide information about Limited members, you need to extract the user IDs from the user groups endpoint
- Since the
- Get the category ID for the expense:
- Use the following endpoint to get the category ID:
GET /workspaces/{workspaceId}/expenses/categories
- Make sure to choose the correct category for the expense
- Use the following endpoint to get the category ID:
- Create the expense:
- Once you have the category ID, you can create an expense using the following endpoint:
POST /workspaces/{workspaceId}/expenses
- Remember to send the request in form-data format, not raw JSON format
- Include the user ID of the Limited member, category ID, and other expense details in the body
- Once you have the category ID, you can create an expense using the following endpoint:
If the request is successful, you will receive a 201 Created
status code.
The expense will be created for the Limited member as expected.