# Hiring Bot
1. Hiring from dribbble manually is time consuming task. Hence, I used selenium and built a bot that can automatically send hiring message
to a candidate. Input will be list of urls of candidate's profiles and message that we want to send.

2. How to setup:
- First make a virtual environment
```
mkdir env
cd env
virtualenv .
source bin/activate
cd ..
```

- we need a driver, if your browser is chrome you need to get a driver of your chrome version. Similarly for other browsers.
Download a chromedriver and paste it in a new directory called assets.

- In input file, paste the url of candidate's profiles

- In template.txt paste your message below Hi (x).

- Run the crawler 
```
python3 dribbble.py -i input_dribble.txt -t template.txt -d assets/chromedriver
```
