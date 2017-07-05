Test home:
    Send a GET request to the home page, and ensure it has the correct amount of blog posts.
    send a GET request to the home view and ensure it responds with the correct route, and a list of blog bosts.
    Send a GET request to the home page, and ensure it has the correct content we wish to see.

Test detail:
    Send multiple GET requests (with IDs) to detail view, and ensure it returns the proper post each time.
    Send multiple GET requests (with IDs) to the detail URL. Ensure that the URL has the correct 
    Send multiple GET requests (with IDs) to the detail URL. Ensure that they have the proper content we wish to see.

Test create:
    Send a GET request to create view, ensure that it returns the create page.
    Send a GET request to create url, ensure that we see the proper content.
    Send a POST request to create view. Ensure that new entry is represented in postgres database.
    Send a POST request to create URL. Ensure that it gets redirected to homepage, and that home page now has the new entry at the top.

Test edit:
    Send multiple GET requests (with IDs) to edit view, and ensure it returns the proper post each time.
    Send multiple GET requests (with IDs) to the edit URL. Ensure that the URL has the correct  content.
    Send a POST request to the edit view, ensure that the postgres database has not changed size, and that the newly edited entry has changed.
    Send a POST request to the edit URL, ensure that it redirects to the detail view, and that the newly edited post is displayed on it.