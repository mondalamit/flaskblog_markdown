# flaskblog_markdown
A blog application that uses markdown for content.
Uses python3.5.

TODO:

1. Make templates modular.
2. Better routing based on titles, not author and entry id.
3. Admin dashboard for creating and editing entries. Maybe use WTForms/PageDown repo by Miguel Grinberg.
4. Add support for tags on posts, and endpoints that show all posts for a given tag so that the sidebar is useful.
5. User authentication for the dashboard, proper encrypted password storage.
6. Pagination support for the home page, as well as "content limiting" to encourage users to go the individual entry's page and save space.
7. Being able to upload/download markdown for entries, when editing or creating a new post.
8. Sessions support so you can accurately track users visiting the page, and collect some user agent data, etc.
9. More custom CSS? Different color scheme?
10. Have an actual production deployment; nginx with gunicorn most likely.
