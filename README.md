# HackNY2017

### APIs used
* Tweepy (tweeting with Python)
* Goo.gl API (shortening source links for character limits)
* New York Times Article Search API (looking for source articles)
* Giphy API (tweet a funny gif at you if your query makes no sense)
* ProPublica (search through congressional records and bills for sources) (not used in final product)

### How it works
* Tweet @FactCheckBotHNY with a query that can be reasonably answered with 'yes' or 'no'
* The tweet is run through New York Times' article search API, and the most relevant result is saved
* A snippet from NYTapi's returned article is run through difflib's SequenceMatcher with the original query
* If the SequenceMatcher returns a match above a reasonable threshold, the bot will tweet back how confident it is that the user's tweet is correct

### Things that were difficult
* NYT API had no documentation for Python, and pip's nytiesarticle module was useless, so we had to manually query using the requests module 
* ^ Same thing for ProPublica's API

### Next time
* Use a wider array of sources than just New York Times
* Find a better way of validating "certainty" than just comparing string deltas (which was pretty hit or miss).
