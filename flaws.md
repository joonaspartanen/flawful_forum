# Application vulnerabilities

## Flaw 1

SQL injections: The application uses raw SQL queries with unsanitized user input. Users can post messages that contain SQL queries, which will be executed in the database. For example, posting a message with body "); DROP TABLE forum_message; -- would delete the whole database table containing the messages. In addition, the application uses the unsafe executescript method that allows executing several queries at once.

Fix: The application should use parameterized queries and escape the user controlled inputs to make sure that no harmful code is executed in the database. The safer execute method should be used instead of executescript.

## Flaw 2

XSS: The messages that users post to the application are not properly sanitized and can contain raw HTML and even scripts. Try posting <script>alert('Hello fool!')</script>.

Fix: The user input should never be trusted. All the content provided by the users input should be sanitized, and all suspicious characters escaped before rendering. In case of Django, it would be enough to remove the '| safe' filter from the forum page template so that the scripts, img tags, links etc. would be rendered as plain text.

## Flaw 3

CSRF attacks: The application uses GET requests to perform certain action that have side-effects, such as logging out. An attacker can easily use links or img tags (even posting them to the forum itself) that cause the user to make GET request to the path "/forum/logout", effectively logging the user out. You can try posting to the forum a message with the following content to see this flaw in effect: <img src='http://localhost:8000/forum/logout/' />

In addition, some other actions, such as logging in and posting messages are performed by a POST requests but they don't require CSRF tokens either.

Fix: Actions with side-effects should use, for example, POST requests and require the presence of a proper CSRF token. In Django, it would be easy to just remove the csrf_exempt decorators and add {% csrf_token %} annotation to the HTML forms.

## Flaw 4

Broken authentication: In the UI, some functionalities are only available to authenticated users. For example, the user must be logged in to see a "DELETE" icon next to their own forum posts. This seems to work fine, but actually the backend-side authentication is broken or missing and even anonymous users can delete posts, for example, using the following curl command: curl -d '{"id": 1}' -H "Content-Type: application/json" -X DELETE http://localhost:8000/forum/posts/

Fix: All the methods that perform actions that belong only to authenticated users should be decorated with Django's login_required annotation. In addition, the post deletion method should check if the user who requests deletion is actually the author of the message to be deleted. Also, the fact that some functionality is not available in the UI does not mean that the attackers don't find a way to exploit it.

## Flaw 5
Exposing sensitive information: The application has a view that contains a list of all the registered users. On the surface, everything looks fine, but examining the browser developer tools' Network-tab, it is easy to see that the user data is fetched from the server as JSON and, in addition to the usernames, it contains lots of sensitive information, such as user emails and even password hashes.

Fix: The server should send only the necessary user data to the browser. On the other hand, instead of sending a JSON response, the users view could be easily and safely rendered with the help of Django templates.

## Flaw 6
The application contains a helper method that creates two test users on startup. This was actually added for testing purposes, but it is of course an obvious vulnerability.

Fix: The source code should never contain hard coded passwords, keys or other secrets. These could be stored in a separate configuration file (such as .env) or in a secure key vault and passed to the application as environment variables.

## Flaw 7
Insufficient Logging & Monitoring: The application does not have logging for suspicious activity or errors.

Fix: Django might have some built-in logging mechanisms, but it would make sense to log information on the action performed by the users, as they might include access to the database. This would make investigating possible breaches and attacks a lot easier.

## Conclusion

Most of the vulnerabilities in the application have been intentionally opened by removing or overriding some of the Django's built-in safety mechanisms. This is a good lesson of the fact that the developers should take advantage of the built-in security mechanisms of the modern web frameworks, such as Django, as many of the most common vulnerabilities have already been dealt with in them. Of course, this does not mean that a modern framework could not contain vulnerabilities: new flaws are discovered – and hopefully patched – continuously both in the frameworks and their dependencies, which is why every developer should make sure to keep their software updated, instead of blindly trusting the framework's safety mechanisms.
