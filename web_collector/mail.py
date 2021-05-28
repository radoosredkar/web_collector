import email
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class row:
    def __init__(self, row_dic):
        self.row_dic = row_dic

    def __str__(self):
        return f""

    def _cell(self, name, value):
        if name == "image":
            return f'<img src="{value}"</img>'
        elif name == "adv_url":
            return f'<a href="{value}"/>'
        else:
            return f"<td>{value}</td>"


html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

part2 = MIMEText(html, "html")


# msg = email.message_from_string('https://www.bolha.com/nepremicnine/stanovanje-osrednjeslovenska-ljubljana-polje-1-sobno-42-m2-oglas-1448607')
msg = MIMEMultipart("alternative")
msg["From"] = "radoosredkar@hotmail.com"
msg["To"] = "radoosredkar@hotmail.com"
msg["Subject"] = "Daily report"
msg.attach(part2)

s = smtplib.SMTP("smtp.live.com", 587)
s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
s.starttls()  # Puts connection to SMTP server in TLS mode
s.ehlo()
s.login("radoosredkar@hotmail.com", "r@Dp1j3mp1v0")

s.sendmail("radoosredkar@hotmail.com", "radoosredkar@hotmail.com", msg.as_string())

s.quit()
