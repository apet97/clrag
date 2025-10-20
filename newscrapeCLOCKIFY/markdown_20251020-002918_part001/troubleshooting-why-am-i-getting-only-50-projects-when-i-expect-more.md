# troubleshooting-why-am-i-getting-only-50-projects-when-i-expect-more

> Source: https://clockify.me/help/troubleshooting/why-am-i-getting-only-50-projects-when-i-expect-more

Why am I getting only 50 projects when I expect more?
Users may report that despite setting a large page-size limit, they only get 50 results. This issue is usually caused by incorrect formatting in the request.
Solution #
- When setting parameters for page-size, ensure there are no spaces before or after the = sign.
- Incorrect:
page-size = 5000
- Correct:
page-size=5000
- Incorrect:
- Incorrect formatting causes the API to default to the 50-page limit.
Once the correct page size is set, you should receive the full set of results.