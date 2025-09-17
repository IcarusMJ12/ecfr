"Thank you so much for taking the time to complete the United States DOGE
Service take-home assessment.

After reviewing your assessment, we have decided to move forward with other
candidates whose skills more closely align with our current needs."

So, about that...

Outside of this section of the readme and the
[assessment.pdf](assignment) converted from docx to pdf, this and the generated
artefacts were my submission to the Department of Government Efficiency (DOGE)
for an unspecified software engineering position.  The following may make more
sense if you read the assignment yourself.

I have previously tried to apply to DOGE online, only to encounter a server
error.  The recruiter, Mr. Grossman, reached out to me independently months
later.  The assignment was supposed to be provided to me early in the week, but
instead after a followup email I received it on a Friday with the deadline
being the following Monday, thereby forcing me to sacrifice my weekend plans.
The submission link for the assignment was supposed to be provided within 24
hours, but like everything else at DOGE so far it didn't take, and after
another followup email I got the link on Monday and a deadline extension til
Tuesday.  I was allowed to request an extension but it's unknown how that would
count against me.

My background, as was clearly established to the recruiter, is as a Python and
C++ backend engineer with relatively minor frontend involvement, and this
particular assignment is largely orthogonal to my skills outside of API
development.

A "simple" website with a backend API that pulls and processes third party data
is definitionally not simple.  An actual simple website, done correctly and
with access to a professional designer, could easily take a couple of days,
while a more complex one could take a backend engineer, a frontend engineer,
and a designer an entire week or longer.  Done properly, it would include
scaffolding, unit tests, integration tests, and a form of deployment.  A 4-6
hour scope, even excluding "setup", is wildly unrealistic, while the open ended
nature of the assignment itself is rather suspicious.

It would have been typical professional courtesy to provide candidates with
common boilerplate that places them on equal footing while also aligning them
with the employer's software stack.  Also, the assignment ought to be only
tangentially, if at all, related to the actual work an employee would be doing.

Charitably, this assessment expects the candidate to be a mind reader that
can complete it with unstated expectations.  Much less charitably, it is a ploy
to crowd source actionable metrics for DOGE without compensation, which is in
violation of the
[https://www.dol.gov/sites/dolgov/files/WHD/fact-sheets/whdfs13.pdf](Fair Labor Standards Act)
which bases employment on "\[t\]he extent to which the services rendered are an
integral part of the principal's business."
Given the unidirectional application of standards unspecified, my
interpretation is leaning towards the latter.

The recruiter didn't claim any confidentiality or ask for an NDA, so only my
sense of ethics would preclude me from sharing my work, and my sense of ethics
does not include suffering fools -- or possibly malicious agents -- gladly.


# eCFR Analysis Website

## Setup

All generated artefacts are included in the archive.  If you wish to generate
them yourself, you'll need `bash`, `npm`, and the latest version of `python3`.

If you're on Windows, maybe [https://www.cygwin.com/](Cygwin) can help.

It's strongly recommended you then pre-warm the cache by running `./ecfr.py` as
that will fetch and analyze all the titles, which takes a while.  From then on
it will only retrieve updated documents.

To generate the artefacts:

```bash
npm install -g @danielx/civet stylus pug-cli
./make_json.py  # to generate the payload
./build.sh  # .civet -> .js, .pug -> .html, .styl -> .css
```


## Running the web server

`python -m http.server 8000` or you may choose to use a different web server
such as Apache.

Then, simply navigate to `localhost:8000` in your browser.
