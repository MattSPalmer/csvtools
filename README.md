# csvtools

This is more an exercise than anything, since the main module probably duplicates a lot of the existing functionality of Python's CSV library.

Nevertheless:

csvtools provides simple analytics on csv files containing report data, chiefly .

The main executable is **callparser**, which parses data from CSV reports generated from IfByPhone, an online call routing service, according to several options.

**-h, --help**: display available options.

**-a, --agents**: display missed calls by agent phone number

**-c, --callers**: display each incoming caller with number of times called

**-m, --missed**: display missed calls by date

**-w, --write**: write input to new file

**-g, --graphbyhour**: graph calls by day and by hour
