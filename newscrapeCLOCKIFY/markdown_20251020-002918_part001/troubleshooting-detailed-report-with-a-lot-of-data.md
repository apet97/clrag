# troubleshooting-detailed-report-with-a-lot-of-data

> Source: https://clockify.me/help/troubleshooting/detailed-report-with-a-lot-of-data

Detailed report with a lot of data
To fetch detailed time entry reports, use the following endpoint:
Add page
and pageSize
parameters to manage large datasets.
Example:
page: 1
pageSize: 1000
If you have more than 1000 entries, create a script or manually change the page number in the body (page: 1
, page: 2
, etc.).