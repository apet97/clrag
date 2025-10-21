# Overview of integrations - Clockify Help

**Source:** https://clockify.me/help/integrations/integrations

Integrations
Clockify Help Center
Integrations
Overview of integrations
In this article
Syncing projects and tasks
Custom domains
Disable integrations
List of Clockify integrations
FAQ
Overview of integrations
5 min read
Start Clockify timer from within other web tools, like
JIRA
,
Trello
,
Asana
,
Todoist
, and others (see
integrations page
for the full list).
User interface displayed in this video may not correspond to the latest version of the app.
Simply install the
Chrome extension
or
Firefox extension
, and a timer button will appear in your favorite web app’s tasks, to-dos, issues, leads, events, etc.
The
browser extension is open-sourced
, so feel free to create new integrations or improve existing ones.
To use JIRA integration, you need to install the
Clockify plugin for JIRA
. Check out
this
Help Center page for detailed instructions.
Syncing projects and tasks
#
The extension can also pick up project name from another app if there’s a project in Clockify with the same name (e.g. you have a
Project X
in both Clockify and Asana/JIRA/Trello/Todoist).
Clockify extension can also create and select projects, tasks, and tags based on the integration:
If there’s a project or task with the same name in Clockify, it will be selected
If there’s no project or task and you have the permission to create it (based on workspace settings), a new one will be automatically created and selected
To enable creation of projects/tasks/tags, you first need to enable it in the extension’s Settings.
Each integration is different. For example, task and project can be created from Asana, Gitlab will also pick up tags, but Gmail won’t do anything except pick up description.
If you need support for this in other integrations, feel free to
contribute code to the extension on Github
.
Custom domains
#
If you use a self-hosted tool that you use on a custom URL (e.g. you use YouTrack on mydomain.com), you’ll need to add your domain and connect it to the corresponding tool:
Open extension
Open settings (hamburger menu in the upper left corner)
Click
Integrations
Scroll down and under
Custom domains
enter your domain (e.g. mydomain.com)
Select the tool that’s on that domain
Click
Add
Disable integrations
#
If you don’t want the button to appear in certain web apps, you can disable it in
Integrations
.
Open the extension
Click on the menu icon in the upper right corner
Click on the
Integrations
button and you’ll jump to the integrations list
Uncheck the apps in which you don’t want to see the
Start timer
button
If you use a self-hosted / on-premise version of some app (like JIRA or Gitlab), at the bottom of the
Integrations
page you can specify the domain where you have the app installed.
List of Clockify integrations
#
Complete list of all the integrations available in Clockify based on their type:
Project management & collaboration
Airtable, Asana, Axosoft, Basecamp, Breeze, ClickUp, ConnectoHub, Fibery, Freedcamp, GetFlow, Group&Work, Jira, Linear, MantisHub, Manuscript, Microsoft Planner, Monday, Notion, Pipefy, Pivotal Tracker, Placker, Podio, Redbooth, Redmine, TeamWave, Teamwork, Trello, Unfuddle, Way We Do, WeKan, Wrike, YouTrack, Zenkit.
Task management
Google Calendar, Infinity, MeisterTask, MyFocusSpace, Nozbe, Outlook, Plaky, Pyrus, TickTick, Todoist, Toodledo.
Communication & support
Cerb, Dixa, Freshdesk, Front, Google Mail, Helprace, Help Scout, Husky Marketing Planner, LiveAgent, Nela, Pixie, Pumble, Slack, Zammad, Zendesk, Zoho Connect.
Development & version control
Azure, Bitbucket, Gitea, GitHub, GitLab, Phabricator, Sentry, Visual Studio.
CRM & sales management
CapsuleCRM, HubSpot, Pipedrive, Salesforce Lightning, Zoho Desk.
Document & note-taking
Coda, Evernote, Google Docs / Sheets, Google Keep, Microsoft Planner.
Time tracking and source management
Clockify, Freshservice, LiquidPlanner, ManageEngine, Microsoft To Do, Plutio, Scoro.
Agile & Kanban
Kanbanize, Rally, Shortcut, Taiga.
Design & prototyping
Figma, Miro.
Workflow automation
Zapier.
Other
Ambra, Connecthub, Crowdin, Freshrelease, Hillia, JetBrains Space, Nifty, OpenProject, osTicker, Sprint.
FAQ
#
I get an error about missing project when I try to stop the timer
#
If you have Timesheet enabled, project is automatically a
required field
. To stop the timer, you’ll have to open your timer and select a project.
Tip: You can set a default project, so each time you start a timer, project is selected automatically (you can enable it by opening the extension and going to Settings).
I’m using an on-premise version of some app
#
No problem. In the extension options, select
Integrations
, scroll down to the bottom, select the tool you’re using (e.g. Gitlab), and enter your custom domain.
Help, I don’t see the button
#
If you don’t see the button, first make sure you’re logged in to the extension. If that doesn’t help, restart the browser. Also, make sure the integration is enabled in URL Permissions (when you open the extension, click on options icon in the upper right corner).
If you’re still experiencing the problem, try these troubleshooting steps:
Remove the extension from your browser
Clear cache and cookies (date range: all time)
Download the latest version of the extension and pin it to the browser
Log in to the extension and enable integration with the app
Check if the button appears in the app
If none of these worked, send us an email and we’ll look into the problem. Sometimes integrations break due to updates in other apps. If you don’t want to wait for us to fix the integration, feel free to help us out by
contributing to our codebase
.
How can I get my favorite tool added?
#
The
extension is open source
so anyone can contribute. If you’ve developed an integration, be sure to let us know so we can feature it on our
Integrations page
.
Adding your tool requires basic web programming skills (HTML, Javascript, Git) and can be done in a couple of hours.
Related articles
#
QuickBooks
JIRA integration
Was this article helpful?
Submit
Cancel
Thank you! If you’d like a member of our support team to respond to you, please drop us a note at support@clockify.me
In this article
Syncing projects and tasks
Custom domains
Disable integrations
List of Clockify integrations
FAQ