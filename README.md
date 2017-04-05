Repository for <http://cleats.racing>.

### How to run
Python 3 is required to run this project. Virtualenv is recommended. To run your own instance of this repository:

```
git clone git@github.com:a-johnston/cleats-racing.git
cd cleats-racing
pip install -r requirements.txt
export FLASK_APP=server.py
flask run
```

Now the page should be running at <http://127.0.0.1:5000>. To run flask in debug mode, run `export FLASK_DEBUG=1` before running. This will automatically restart the server with code changes and give much more verbose output.

### Customization
To customize this repository for your own race/ride series, simple changes can be made through `config.py`. For example, to change the title of the site, modify the `SITE_TITLE` line. Data is loaded off of Google Sheets and should follow a specific format:
 - The first row contains the names of individual races/rides (not necessarily adjacent)
   * The first and second columns of the first row are ignored
 - The first and second column of the second row contain "ID" and "Name" respectively
 - The second row contains the names of intermediate events of each race/ride
   * Event titles must be categorized as Sprint, KOM, QOM, or GC to be included in results
   * For example, "KOM:Some Local Climb"
   * Events are associated with the ride with the greatest column number greater or equal to the event column number
 - Every subsequent row defines a rider and their results on individual events
   * Rider ID (first column) can be any valid Python string (for example, a racing license)
   * Rider results (third column onward) can be either an integer or blank

An example of this format can be found on the [RSWNR results spreadsheet](https://docs.google.com/spreadsheets/d/11uhc4wGjhvH5T-M6RTt9kyMA6oDoEJrDjxZZo_7chuA/edit?usp=sharing).

### Deploying with NGINX and uWSGI
Included in `example_conf` are basic configuration files for NGINX and a uWSGI systemd service. The systemd service assumes the repository is located at `/www/cleats-racing` and uses a virtualenv `venv/` and must be modified if this is not the case for your particular instance.

The NGINX configuration file is extremely basic and for production should at least be modified to serve static files directly rather than delegating static file requests to flask.

Additionally, there is a webhook file `hooks.json` which uses [Adnan Hajdarević's `webhook` tool](https://github.com/adnanh/webhook). Currently it runs a redeploy script for very simple CI/CD with GitHub, for example. This can be run by `<go path>/bin/webhook -hooks example_conf/hooks.json -verbose`.
