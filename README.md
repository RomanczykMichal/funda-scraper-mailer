# funda-scraper-mailer
The script is able to search the latest ads for rental apartments, condos and houses on funda.nl. The latest ads will be sent via a pre-configured email. In order to set up the email correctly, you need to set up a new mailbox on Gmail and then obtain the application's password. To do this, I recommend using the method described in this video https://www.youtube.com/watch?v=g_j6ILT-X0k&t=2s&ab_channel=ThePyCoach (0:25 - 2:45).

Translated with www.DeepL.com/Translator (free version)

To run this commit instal forked version of funda scraper.
```bash
    pip install --upgrade --force-reinstall -r requirements.txt
```

Arguments list (bolded are required):
**  - '-t' - time interval between messeges (in minutes).
  - '-a' - area to search.
  - '-m' - email of receiver.**
  - '-n' - number of pages to search.
  - '-r' - additional range to search.
