### A Simple URL scraper 
a simple tool design to scrape a html (local) document and send all the links within it to some endpoint

### Usage
the scraper expects some arguments upon launch. all arguments must be passed in the command line upon launchiing the script.
the first argument is the endpoint to `POST` messages to. in the context of discord - that would be a webhook url. said url _must be kept as secret!_.
creating a webhook endpoint is explained [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

all following arguments are paths to a local html document one wants to scrape.

an example might look like: `python url_scraper.py https://discord.com/api/webhooks/secret path/to/html/document_1.html path/to/html/document_2.html`

### Setting up
- make sure you have python 3.8 installed
- clone the repo
- navigate to the project directory, open a terminal and run `python3 -m venv .venv`. this will create a virtual environment in the current directory (which may take a few seconds)
- run `source .venv/bin/activate` to activate the virtual environment (`.venv\Scripts\activate.bat`). [`deactivate` in case you want to deactivate it]
- within the virtual enviroment run `pip3 install -r requirements.txt`. this will install all the necessary modules to the virtual environment 
- run `python url_scraper.py` with all the necessary arguments