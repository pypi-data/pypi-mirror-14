# -*- coding: utf-8 -*-
import logging
import logging.handlers


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string  # For 'tls', add this line

            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time

            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT

            smtp = smtplib.SMTP(self.mailhost, port)

            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                string.join(self.toaddrs, ","),
                self.getSubject(record),
                formatdate(), msg
            )

            if self.username:
                smtp.ehlo()  # For 'tls', add this line
                smtp.starttls()  # For 'tls', add this line
                smtp.ehlo()  # For 'tls', add this line
                smtp.login(self.username, self.password)

            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def init_log(file_name=None, email_auth=None, level='INFO'):
    """Initializes the log file in the proper format.

    Args:
        filename (str): Path to a file. Or None if logging is to
                        be disabled.
        email_auth (dict): email credentials
        toaddrs (list): email address recipients
    """
    logger = logging.getLogger(__package__)
    logger.setLevel('DEBUG')

    template = "[%(asctime)s] %(levelname)-8s: %(name)-25s: %(message)s"
    formatter = logging.Formatter(template)

    # log info and warnings to file (or stderr)
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if file_name:
        handler = logging.handlers.RotatingFileHandler(file_name, backupCount=5)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # log errors and exceptions to email
    if email_auth:
        mail_handler = TlsSMTPHandler(
            mailhost=email_auth['server'],
            fromaddr=email_auth['username'],
            toaddrs=email_auth['to'],
            subject="O_ops... mip2scout failed!",
            credentials=(email_auth['username'], email_auth['password'])
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
          '%(asctime)s - %(name)s - %(levelname)s: %(message)s '
          '[in %(pathname)s:%(lineno)d]')
        )
        logger.addHandler(mail_handler)
