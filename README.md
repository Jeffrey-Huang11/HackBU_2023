# HackBU_2023
Annual hackathon event hosted by Binghamton's HackBU club

## Members:
- Anthony Zhang (azhan134@binghamton.edu)
- Jeffrey Huang (jhuan262@binghamton.edu)
- Julian Ortiz (jortiz53@binghamton.edu)
- Klejben Hysenbelli (khysenb1@binghamton.edu)

## Hack:
Utilizes machine learning to determine the safety of a website given its URL. Combining pre-existing databases labeling websites as 'good' or 'bad' with Beautiful Soup (an HTML parser in python), we determined metrics to check the safety of a website. These metrics are moved to a csv file, and the data is used to train our algorithm by finding correlations and weighing metrics. 

### Metrics:
- url 
- url_length 
- https (https or http)
- number of outgoing links 
- number of safe outgoing links 
- number of non-safe outgoing links 
- length of content (total number of chars)
- status (whether site is currently up or down)
- tld (domain name)
- sentiment analysis (positive or negative) 
- label ()
