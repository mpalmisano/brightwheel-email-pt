# BrightWheel

### To install and run the application
1. Navigate to the repository, create a virtual environment (e.g. `python3 -m venv env`), and install the requirements 
   (e.g. `pip3 install -r requirements.txt`).
2. Run `python3 -m flask run` in a terminal to start up Flask.
3. Open up an API tester application like Postman and send a `POST` request to `localhost:5000/email` with an example 
   payload.

### Language, framework and libraries rationale
- I chose to do this exercise in Python3 because it is the language that I am most familiar with and because it makes 
  it fairly easy to build a basic API quickly.
- For a similar reason, I chose to implement the API using `Flask`.  Again, it was the framework I was familiar with, and 
  it is fairly lightweight to implement and API with.  The `Flask-RESTful` extension is helpful and so was added for 
  additional ease.
- I used the `html2text` library to parse the HTML to plain text.  I figured there was a library already implemented for
  such a task as this so I looked it up and sure enough there was.  No reason to reinvent the wheel.  
- I used the `requests` library to implement the email service provider client wrappers because it seems to be fairly
  standard to use for sending requests to APIs from what I have seen, and I've worked with it before.  

### Tradeoffs, anything that was left out, and what I would do differently if I had additional time
- I used a fairly naive regular expression to check the validity of the email addresses.  I did this largely for 
  the sake of time.  If this were in production, you would want to include a regular expression that catches more edge
  cases (e.g. special characters that are not allowed).
- If this were being implemented in production, I imagine that functions like the validations for example would be 
  pulled out into a general common repository or package for use in multiple applications across the codebase.  To 
  simulate this and to organize the code a bit clearer, I pulled the validations and transformations out of app.py and 
  chose to import the functions.  
- I implemented the email service provider wrappers very quickly to try to abstract away some of that setup and also 
  because those would be good to be reusable if this application was fully built out.  I definitely implemented them 
  quickly (and a bit messy) for the sake of time and there is definitely room for improvement there. 
- If I had more time, I would have abstracted the Snailgun email status checking a bit nicer.  As is, it is a bit rough.
  Along a similar line, there are commonly used decorators that help make API calls and the like more robust through
  structuring the retries.  If I had more time, I would have invested in implementing those.  
- If I had had more time, I probably would've implemented the application via Docker Compose to make it a bit more 
  robust to set up and run.
- As always, more thorough documentation would be best if given more time.  

### Other
- All in all, I enjoyed the exercise!  I am sure there is a lot that can be improved on my code here, but I appreciated 
  the challenge and look forward to hearing some feedback!
