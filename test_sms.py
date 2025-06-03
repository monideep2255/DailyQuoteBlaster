import os
import unittest
from unittest.mock import patch, MagicMock

import send_sms

class SendSMSTestCase(unittest.TestCase):
    @patch('send_sms.Client')
    def test_send_quote_sms_success(self, mock_client_cls):
        # Setup Twilio credentials
        creds = {
            'TWILIO_ACCOUNT_SID': 'AC123',
            'TWILIO_AUTH_TOKEN': 'token',
            'TWILIO_PHONE_NUMBER': '+10000000000',
        }
        with patch.dict(os.environ, creds, clear=True):
            mock_client = MagicMock()
            mock_message = MagicMock(sid='SM123')
            mock_client.messages.create.return_value = mock_message
            mock_client_cls.return_value = mock_client

            result = send_sms.send_quote_sms(
                to_number='+15555555555',
                quote_text='hello',
                quote_author='author',
                category='general'
            )

            self.assertTrue(result)
            mock_client.messages.create.assert_called_once_with(
                body=send_sms.create_sms_template('hello', 'author', 'general'),
                from_='+10000000000',
                to='+15555555555'
            )

    @patch('send_sms.send_quote_sms')
    def test_test_sms_delivery_uses_send_quote_sms(self, mock_send):
        mock_send.return_value = True
        number = '+15550001111'
        result = send_sms.test_sms_delivery(number)

        mock_send.assert_called_once_with(
            to_number=number,
            quote_text="This is a test quote to verify SMS delivery.",
            quote_author="Daily Quote Sender"
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
