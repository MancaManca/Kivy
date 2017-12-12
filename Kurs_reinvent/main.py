from time import time
from kivy.app import App
import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, Clock, BooleanProperty, ListProperty, \
	partial, Logger
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')

class CustomPopup(Popup):

	mode = ObjectProperty()

# Dispatch event on_active checkbox to Popup ModeState label & update store JSON value
	def set_flag_edit(self,instance,value):

		# print(value)
		MainView.store['flag_add_edit'] = {'value':'{}'.format(value)}
		# print(MainView.store.get('flag'))

	pass

	def set_flag_clean(self,instance,value):
		MainView.store['flag_clean'] = {'value': '{}'.format(value)}
		# print('clean flag val')
		# print(value)

		if value:
			self.ids.paycheck_amount_clean.opacity= .9
			self.ids.paycheck_amount_clean.readonly = False
			self.ids.update_paycheck_amount.opacity = .9
			MainView.changed_values_dic = {}
		else:
			self.ids.paycheck_amount_clean.opacity = 0
			self.ids.paycheck_amount_clean.readonly = True
			self.ids.update_paycheck_amount.opacity = 0
			MainView.store['paycheck_amount'] = {'value': MainView.store['init_paycheck_amount']['value']}



	def set_paycheck_amount_clean(self,pay_amount,state):
		if state:
			# print(pay_amount)
			if len(pay_amount)>1:
				MainView.store['paycheck_amount'] = {'value': int(pay_amount)}
				self.ids.paycheck_amount_clean.text = ''
				self.ids.paycheck_amount_clean.hint_text = ''

				# print(state)
				# print(MainView.store['paycheck_amount'])
			else:
				self.ids.paycheck_amount_clean.hint_text = 'invalid amount'
		# else:
		# 	MainView.changed_values_dic['paychechk_ammount']=None
		# 	print(MainView.store['paycheck_amount'])

class MainView(BoxLayout):

# Storing current value for edit mode True Fals. Initialy populated by on start with False.
# Updated  with Custom Popup set_flag_edit event dispatch
	store = JsonStore('edit_mode.json')
	avg_rates_list = ListProperty()
	avg_rates_list_converted = ListProperty()
	removal = ObjectProperty()

# Disctionary used to calculate final values
	changed_values_dic = DictProperty(None)


	def __init__(self, **kwargs):
		super(MainView, self).__init__(**kwargs)
		if self.store.exists('init_paycheck_amount'):
		# MainView.remove_widget(MainView.ids.init_s)
		# 	print('uso')
			self.remove_login()

# Event dispatched  triggered on Save button clicked
# First arg taken from Input Expanse Name , second arg taken from Input Expense Amount
# Adding values to Main View dic object changed values
# Clearing Input Expense Name and Input Expense Amaount text
	def remove(self,init_am_v):
		if len(init_am_v)>2:
			self.remove_login()
			MainView.store['paycheck_amount'] = {'value': int(init_am_v)}
			MainView.store['init_paycheck_amount'] = {'value': int(init_am_v)}
			# print(self.children)
		else:
			self.ids.init_s_input.hint_text='Wrong Value!'
	def save_entry(self,ex_n,ex_v):

		if len(ex_n) & len(ex_v) > 0:

			self.changed_values_dic[ex_n] = int(ex_v)
			self.ids.test.text = str(ex_n)
			self.ids.f_expense_input.text = ''
			self.ids.f_expense_v_input.text = ''

# Clear all labels from Widget displaying Expenses dict values added as Label widget
	def clear_all(self):

		self.ids.dic_values_wrap.clear_widgets()

# Add Main View dict changed_values_dic values as Labels
	def show_edits(self):

		self.clear_all()

		for i in self.changed_values_dic:
			self.ids.dic_values_wrap.add_widget(Label(text='{} {}'.format(i, self.changed_values_dic[i]),color=(1,1,1,1)))

# Get data from url, event triggered by on_click GET button

	def remove_login(self):

		self.remove_widget(self.ids.init_s)
		self.ids.main_v.size_hint_y = 1
		self.ids.main_v.opacity = 1

	def send_request(self,*args):

		search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
		# print search_url
		self.request = UrlRequest(search_url, self.get_avg_rates,on_error=self.on_error,on_failure=self.on_failure,on_progress=self.on_progress) # <2>

	def on_error(self,request,*args):

		# print (args)
		# print ('on error {}'.format(request.result))
		return False
	def on_failure(self,request,*args):

		# print (args)
		# print ('on failure {}'.format(request.result))
		return False
	def on_progress(request,current_size,total_size,*args):

		return True
		# print('Progress {} {}'.format(current_size,total_size))


	def get_avg_rates(self,request,*args):
		l =[]

		anchorStart, anchorEnd = makeHTMLTags("td")
		htmlText = request.result
		anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd

		for tokens, start, end in anchor.scanString(htmlText):
			l.append(tokens.body)

		baba = None
		deda = None

		for i, j in enumerate(l):
			if j == 'EUR':
				baba = i + 2
			if j == 'USD':
				deda = i + 2
		#############################################################

		# print('{}'.format(l))
		eur = l[baba]
		conv_eur = str(eur)
		# self.avg_rates_list_converted.append(conv_eur)

		# print ('{}'.format(conv_eur))
		dol = l[deda]
		conv_dol = str(dol)
		# self.avg_rates_list_converted.append(conv_dol)


		self.store['rates'] = {'eur': conv_eur, 'dol': conv_dol}
		self.populate()

	# def populate(self,request,*args):
	#     print()
	def calculate(self,stored_eur_rate,stored_dol_rate,paycheck_amount=1350):
		# print(self.store.exists('paycheck_amount'))
		# for key in self.store:
			# print(self.store[key])
			# print(self.store.keys())
		if self.store.exists('paycheck_amount'):
		# 	print('entered if calculation')
			try:
				paycheck_amount = int(self.store['paycheck_amount']['value'])
			except KeyError:
				# print('No current entry for paycheck')
				pass
		exp_sum = sum(self.changed_values_dic.values())
		# print(exp_sum)
		pay_sum = float(float(stored_dol_rate) * paycheck_amount)
		# print(pay_sum)
		left_sum = float(float(stored_dol_rate) * paycheck_amount) - float(exp_sum)
		# print(left_sum)


		self.ids.avg_rate_dol_value.text = str(stored_dol_rate)
		self.ids.avg_rate_eur_value.text = str(stored_eur_rate)
		self.ids.paycheck_value.text = str(pay_sum)
		self.ids.expenses_value.text = str(exp_sum)
		self.ids.clean_leftover_value.text = str(left_sum)
	def populate(self):
		# print(self.store['rates'])



		self.calculate(self.store['rates']['eur'],self.store['rates']['dol'])


	# def control_content(self):
	# 	a=True
	# 	b= True
	# 	default_setup_dic = {'porez': 22400,
	# 			'stan': float(self.store['rates']) * 225,
	# 			'osiguranje': 3000,
	# 			'kuca': 20000,
	# 			'racuni': 10000,}
	#
	# 	if a & b:
	# 		print('Should be edit clean mode')
	# 	if a == False & b:
	# 		print('Should be default with adding edit')
	# 		for key in default_setup_dic:
	# 			self.changed_values_dic[key] = default_setup_dic[key]
	# 		# self.changed_values_dic = default_setup_dic




class PaycheckApp(App):
	time = NumericProperty(0)

	def build(self):

		Clock.schedule_interval(self._update_clock, 1 / 60.)
		root = BoxLayout(orientation='vertical')
		root.add_widget(MainView())



		return root

	def on_pause(self):

		return True

	def on_start(self):

# Set initial value of FALSE to Main View store and Values for eur dol
		if MainView.store.exists('init_paycheck_amount'):
			# MainView.remove_widget(MainView.ids.init_s)
			# print('uso')

			MainView().ids.init_s.size_hint_y = 0
		mv = MainView()

		if not MainView.store.exists('flag_add_edit'):
			MainView.store['flag_add_edit'] = {'value':'False'}
		# else:
			# print 'Flag Edit exists'

		if not MainView.store.exists('flag_clean'):
			MainView.store['flag_clean'] = {'value': 'False'}
		# else:
			# print('Flag Clean exists')

		if not MainView.store.exists('paycheck_amount'):
			MainView.store['paycheck_amount'] = {'value': 1350}

			# mv.remove_widget(mv.ids.init_s)

			# print(mv.ids)
			# print(MainView().ids.init_s)
			# print(MainView())
			# MainView.remove_widget(MainView.removal)
		Clock.schedule_once(partial(mv.send_request,'self'), 1)

		# print(MainView.store.get('flag'))
		# print(MainView.store.get('rates'))
	# MainView.store['paycheck_amount'] = {'paycheck': 1350}

	def _update_clock(self, dt):

		self.time = time()

	def show_popup(self):

		p = CustomPopup()
# Set initial Label value from store json. Updated Label on Popup open with latest value in store JSON
		p.ids.mode_state.text = str(MainView.store.get('flag_add_edit')['value'])
		# print(MainView.store.get('flag_add_edit'))
# Set Checkbox value on Popup open , value taken from store JSON
		if MainView.store.get('flag_add_edit')['value'] == 'True':
			p.mode_edit.active = True
		if MainView.store.get('flag_clean')['value'] == 'True':
			p.mode_clean.active = True
		p.ids.paycheck_amount_clean.hint_text = str(MainView.store['paycheck_amount']['value'])
		# print('Edit Checkbox status is {}'.format(p.mode_edit.active))
		# print('Clean Checkbox status is {}'.format(p.mode_clean.active))
		p.open()
	pass

if __name__ == '__main__':

	PaycheckApp().run()






