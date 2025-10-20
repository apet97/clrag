# projects-import-clients-projects

> Source: https://clockify.me/help/projects/import-clients-projects

Import projects & clients
You can mass import projects, clients, tasks, and tags to Clockify from a file.
This feature is available on a free plan. Only admins can import data.
If you have a paid subscription, you can also import time entries.
How to import data #
- Go to Settings > Import tab
- Click Upload CSV file and select file from your computer
- Review how many items will be created and click Start import
- When finished, you’ll get a confirmation message
Required CSV format #
- Values need to be comma-separated
- Columns must have headers in English. Values: Client, Project, Task, Tags
- Maximum file size is 1 MB
CSV file example #
You can create a CSV file: By opening an Excel file and then go Save as and choose CSV format; or by opening a plain text editor (like Notepad) and putting headers in the first row (where you separate values with a comma), and listing values in new rows.
Project, Client, Task, Tags ProjectA1,ClientA,, ProjectB1,ClientB,, ProjectB2,ClientB,TaskB1, ProjectC1,,TaskC1, ProjectC2,,TaskC1,Tag1 ,,,"Tag2,Tag3"
Notes #
- File can have a single column or their combination (task column requires at least project column)
- If you don’t group projects by Client, the column name must match what you’ve set in workspace settings (e.g. department, category…)
- The order of the columns is not important. Names are case sensitive.
- Multiple tags can be imported by surrounding tags in double quotes and separating with a comma (e.g. “tag1, tag2, tag3”)
- If an item already exists, it will be skipped during the import. Only items that don’t already exist will be created.
- When you upload a file, it will be first analyzed. If there’s an error, you’ll get a message and won’t be able to proceed.
- You can import only projects, clients, or tags by creating a CSV file with a single column.
- You can import projects and their respective client by including both columns.
- If you import tasks, you need its project column.
- Projects will inherit initial private/public and billable/non-billable status based on New projects are by default workspace settings.
Max character limits #
- Task: 1,000
- Project: 250
- Client: 100
- Tag: 100
Import multiple tasks #
You can import multiple tasks for the same project by including an additional line for the same project and specifying a different task.
Project,Client,Task
ProjectA,ClientA,Task1
ProjectA,ClientA,Task2
ProjectA,ClientA,Task3
You can also add a task in bulk to existing projects:
- Go to Summary report
- Group by Project / (None)
- Select a long date range
- Export as CSV
- Open CSV in Excel or Google Sheets
- Delete time columns
- Add Task column and write new task name everywhere
- Save as CSV
- Import the new CSV file
If you’d like to import multiple tasks in a single project as a CSV file, you need to list all tasks in the task column and put the project with the same name beside every task. Tasks are then imported one by one and the system reads the task name and associates it with the project that is in the project column in the given row.