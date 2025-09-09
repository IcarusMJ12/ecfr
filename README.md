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
