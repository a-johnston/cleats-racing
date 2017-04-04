Repository for <http://cleats.racing>.

Python 3 is required to run this project. Virtualenv is recommended. To run your own instance of this repository:

```
git clone git@github.com:a-johnston/cleats-racing.git
cd cleats-racing
pip install -r requirements.txt
export FLASK_APP=server.py
flask run
```

Now the page should be running at <http://127.0.0.1:5000>. To run flask in debug mode, run `export FLASK_DEBUG=1` before running. This will automatically restart the server with code changes and give much more verbose output.

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
