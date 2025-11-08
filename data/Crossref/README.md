# Crossref

https://api.crossref.org/works?query=radiomics
https://api.crossref.org/works?query=radiomics&filter=update-type:retraction


Crossref has no boolean operations, what they do is some kind of 'take 20%' of best scores/matches.
Therefore the search was restricted to the term ‘radiology’ only.

https://api.crossref.org/works?filter=from-pub-date:2012-01-01,until-pub-date:2026-01-10&query=radiology
https://api.crossref.org/works?filter=from-pub-date:2012-01-01,until-pub-date:2026-01-10,update-type:retraction&query=radiology
