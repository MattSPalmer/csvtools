# csvtools

This is more an exercise than anything, since the main module probably
duplicates a lot of the existing functionality of Python's CSV library.

Nevertheless:

csvtools provides simple analytics on csv files containing report data.

The main executable is **callparser**, which parses data from CSV reports
generated from IfByPhone, an online call routing service, according to several
options.

**-h, --help**: display available options.

**-a, --agents**: display calls by agent per day

**-c, --callers**: display each incoming caller with number of times called

**-m, --missed**: display missed calls by date

**-w, --write**: write call details (date to the hour and whether they were
answered) to a JSON file

**-g, --graphbyhour**: graph calls by day and by hour

# desk API

This repo also contains tools which allow for the retrieval of data from Desk.com

*This is a work in progress.*
