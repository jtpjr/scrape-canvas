# Canvas scraper
Forked from [john-hix](https://github.com/john-hix/scrape-canvas) > [Koenvh1](https://gist.github.com/Koenvh1/6386f8703766c432eb4dfa19acdb0244) > jtpjr

# Changes from upstream:
**Implemented:**
* Will create folders from "pages", for a more familiar navigation. 

**Not yet implemented:**
* Download videos* from links
* Download embedded videos*
* Fix handling of special characters see [issue](https://github.com/MrRinkana/scrape-canvas/issues/3#issue-1070045519)

\*Currently only videos from "instructuremedia.com/embed/"

# Features
* TODO

# Please double-check the data
Please make sure you can view all resources offline without connecting to a server
before calling your import done. This script does not cover all cases! You may need to fix/download things manually!

# Running:
* Install python 3+ if not already installed.
* Get a access token from your settings page (canvas).
* Run as a script: ```python canvas-scraper.py link_to_your_canvas your_access_token output_path course_ids```
  - For the link, use **https!** Othervise your token will be sent **unecrypted**.
  - The script fill create the output folder if it does not exist.
  - The script will overwrite earlier files that have the same name as what is being written (if run previously in same location)
  - For the course_ids, it is the last number in the course homepage link, separate multiple with commas.
* You may need to install missing libraries with ```pip install```. (probably ```pip install canvasapi```)
