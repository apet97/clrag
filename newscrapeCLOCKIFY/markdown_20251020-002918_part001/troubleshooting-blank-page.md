# troubleshooting-blank-page

> Source: https://clockify.me/help/troubleshooting/blank-page

Blank page or ‘something went wrong’ message
If you are experiencing a blank page or you’re getting the message ‘something went wrong’ on the login screen, this issue is often related to your network connection.
Check your firewall and VPN settings #
Your firewall or VPN might be blocking access to our site, and therefore, it’s advisable to check whether the Clockify app is allowed access.
Your network connection is not stable #
Try connecting to a different network, such as a mobile hotspot or a different WiFi connection, to see whether the issue persists.
Browser issues
Make sure that your browser is up to date and that you’re running the latest version. Additionally, clearing the cache and cookies might also help resolve the issue.
Here’s how to clear the cache on different browsers:
- Google Chrome
- Click the three-dot menu in the top-right corner
- Go to Settings
- Click Privacy and security on the left sidebar
- Select Delete browser data
- Select “all time” under the time range
- Delete
- Safari
- Launch the Safari browser on your Mac.
- Select Safari → Preferences
- Click the Privacy tab and select Manage Website Data
- Select a website that is listed, then click Remove. To remove all website data from Safari, click Remove All.
- Firefox
- Click the menu button to open the menu panel.
- Click History → select Clear Recent History
- Next to Time range to clear, choose Everything from the drop-down menu, select Cache in the items list, make sure other items you want to keep are not selected, and then click the OK button.
- Microsoft Edge
- In Edge, select More (three horizontal dots in the upper right corner).
- Select Settings → Open the Settings on the left-side menu → Privacy, search, and services.
- Select Choose what to clear under Clear browsing data.
- Under Time range, choose a time range “All time”.
- Select Cookies and other site data, and then select Clear now.
To ensure that all data is deleted and that your browser is running properly, make sure to select ‘all time’ when clearing the cache.
Whitelist Clockify domains and IP addresses #
If you’re using a restricted network (e.g., corporate or secure office network), you may need to whitelist specific Clockify domains to allow the login page to load properly.
Make sure the following domains and IPs are allowed in your firewall or network settings:
- img.clockify.me
- api.clockify.me
- global.api.clockify.me
- reports.api.clockify.me
- stomp.clockify.me
- IP address: 198.2.128.220
How to whitelist
- Identify where to manage network access (firewall, proxy, security software, etc.)
- Add the domains and IP addresses listed above to your allowed list
- Save the changes and refresh the login page
Still having issues? The Clockify Support Team will be happy to look into it and assist you further. Please contact us at support@clockify.me and provide us with the following information:
- Browser and browser version
- Whether you’re using a VPN or a Firewall