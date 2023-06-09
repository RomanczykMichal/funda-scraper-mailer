import ssl
import smtplib
from email.message import EmailMessage

class Mailer:

    @staticmethod
    def send_mail(email_sender, email_receiver, email_pass, subject,  data):
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        body = Mailer.prepare_body(data)
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_pass)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        del(body)
        del(em)
    
    @staticmethod
    def prepare_body(data):
            list = ""
            for index, row in data.iterrows():
                #list += (f'https://www.funda.nl/huur/{row["city"]}/{row["house_type"]}-{row["house_id"]}-{str(row["address"]).lower().replace(" ", "-")}\n')
                list += f'{row["url"]}\n'
            return list