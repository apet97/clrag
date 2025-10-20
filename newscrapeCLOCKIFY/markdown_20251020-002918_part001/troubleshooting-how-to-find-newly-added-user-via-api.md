# troubleshooting-how-to-find-newly-added-user-via-api

> Source: https://clockify.me/help/troubleshooting/how-to-find-newly-added-user-via-api

How to find newly-added user via API?
1 min read
When you add a user to a workspace via API, you may want to identify the new user in the returned memberships array.
Solution #
- Check the last entry:
The newly added user will always be the last item in thememberships
array.
You can also identify the userID
by checking the last entry in the list of returned memberships.
Was this article helpful?
Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me