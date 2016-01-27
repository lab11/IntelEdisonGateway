



GPIO_RED   = 13
GPIO_GREEN = 12
GPIO_BLUE  = 182

PWM_RED   = 1
PWM_GREEN = 0
PWM_BLUE  = 2

LED_RED = 0
LED_GREEN = 1
LED_BLUE = 2

class EdisonGatewayLEDs ():

	pwm_numbers = [PWM_RED, PWM_GREEN, PWM_BLUE]

	def __init__ (self):
		self.enable_gpio(GPIO_RED)
		self.enable_gpio(GPIO_GREEN)
		self.enable_gpio(GPIO_BLUE)

		self.configure_pwm(GPIO_RED, PWM_RED)
		self.configure_pwm(GPIO_GREEN, PWM_GREEN)
		self.configure_pwm(GPIO_BLUE, PWM_BLUE)

		# Init all PWM off
		self.set_pwm(PWM_RED, 0)
		self.set_pwm(PWM_GREEN, 0)
		self.set_pwm(PWM_BLUE, 0)
		self.enable_pwm(PWM_GREEN, False)
		self.enable_pwm(PWM_RED, False)
		self.enable_pwm(PWM_BLUE, False)

	# Enable the three relevant GPIOs
	def enable_gpio (self, gpio):
		try:
			with open('/sys/class/gpio/export', 'w') as f:
				f.write('{}'.format(gpio))
		except IOError:
			print('Already exported GPIO{}'.format(gpio))

		with open('/sys/class/gpio/gpio{}/direction'.format(gpio), 'w') as f:
			f.write('out')
		with open('/sys/class/gpio/gpio{}/value'.format(gpio), 'w') as f:
			f.write('1')

	# Configure all three pins to be PWM
	def configure_pwm (self, gpio, pwm):
		try:
			with open('/sys/class/pwm/pwmchip0/export', 'w') as f:
				f.write('{}'.format(pwm))
		except IOError:
			print('Already exported PWM{}'.format(pwm))

		with open('/sys/kernel/debug/gpio_debug/gpio{}/current_pinmux'.format(gpio), 'w') as f:
			f.write('mode1')

	def enable_pwm (self, pwm, enable=True):
		with open('/sys/class/pwm/pwmchip0/pwm{}/enable'.format(pwm), 'w') as f:
			f.write('{}'.format(1 if enable else 0))

	def set_pwm (self, pwm, duty_cycle):
		period = 4950495.0
		dc = int((float(duty_cycle) / 100.0) * period)
		with open('/sys/class/pwm/pwmchip0/pwm{}/duty_cycle'.format(pwm), 'w') as f:
			f.write('{}'.format(dc))

		if duty_cycle == 0:
			# To turn off we disable PWM
			self.enable_pwm(pwm, False)
		else:
			# Otherwise make sure it is on
			self.enable_pwm(pwm)

	def on (self, led, brightness):
		self.set_pwm(self.pwm_numbers[led], brightness)

	def hex (self, hex):
		if len(hex) == 6:
			def to_brightness(hex_chunk):
				return int((float(int(hex_chunk, 16)) / 255.0) * 100.0)
			r = to_brightness(hex[0:2])
			g = to_brightness(hex[2:4])
			b = to_brightness(hex[4:6])

			self.on(LED_RED, r)
			self.on(LED_GREEN, g)
			self.on(LED_BLUE, b)
