import requests  # http request
from bs4 import BeautifulSoup  # web scrapping
import smtplib
# send the mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()

# email content placeholder
content = ""


# extracting Hacker News Stories

def extract_news(url):
    print("Extracting Hacker News Stories.....")
    cnt = ''
    cnt += ("<b>Hacker News Top Stories:</b>\n" + "<br> " + "-" * 50 + "<br>")
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i + 1) + '::' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        # print(tag.pretify # find_all('span' , attrs={'class':'sitestr'}))
    return (cnt)


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------------<br>')
content += ('<br><br>End of the message')

# send the mail
print("Sending the mail.....")
# outlook mail details
SERVER = 'smtp.office365.com'
PORT = 587
FROM = 'your_email' # sender email
TO = 'recipient' # receiver email and can be a list
PASS = '*******' # email password


msg = MIMEMultipart()
msg['subject']= 'Hacker News Top Stories [Automated Email]'+' '+str(now.day)+'/'+str(now.month)+'/'+str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
print('Initializing servers..........')

server = smtplib.SMTP(SERVER, PORT)
server.debuglevel = 1
server.ehlo(1)
# start tls connection
server.starttls()
# login to the email account
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())
print('Mail sent successfully')
server.quit()
