
import le910_serial
import signal
import sys

def send_sms(number, message):
    try:
        le910 = le910_serial.le910_serial()
    except:
        exit()

    def signal_handler(signal, frame):
        print('Exiting program...')
        le910.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # clear serial data buffer
    le910.clear_data_buf()

    # get model name from the modem
    le910.write('get_model_name')
    model_name = le910.get_data_block()
    if le910.get_data_block() != 'OK':
        le910.stop()
        exit()

    # set text mode parameter, only required for SVG modem
    if 'SVG' in model_name:
        le910.write('set_text_mode_parameter')
    if le910.get_data_block() != 'OK':
        le910.stop()
        exit()

    # set message format to TEXT mode
    le910.write('set_message_format')
    if le910.get_data_block() != 'OK':
        le910.stop()
        exit()


    # send SMS message
    print('Send message to number: {:}'.format(number))
    le910.write('send_message', '\"' + number + '\"\r\n')
    le910.write('sms_body', message + '\x1a')
    # READ BACK: AT+CMGS="phone number", but I don't care this
    le910.get_data_block()
    print('SMS sent')

    le910.stop()
