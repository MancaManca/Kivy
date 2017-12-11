from time import time
from kivy.app import App
import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, Clock, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')


class CustomPopup(Popup):

	mode = ObjectProperty()

	def print_l(self,instance,value):

		self.mode.text = str(value)
		MainView.store['flag'] = {'value':'{}'.format(value)}
		print(MainView.store.get('flag'))

	pass

class MainView(BoxLayout):

	store = JsonStore('edit_mode.json')
	mode_s = ObjectProperty()
	changed_values_dic = DictProperty(None)
	# ac = BooleanProperty(False)
	# changed_values_dic = {
	# 	'porez'     : 22400,
	# 	'stan'      : float(200) * 225,
	# 	'osiguranje': 3000,
	# 	'kuca'      : 20000,
	# 	'racuni'    : 10000,
	# }
	# if CustomPopup.boo == False:
	# 	print(CustomPopup.boo)
	# 	changed_values_dic = DictProperty()
	def save_entry(self,ex_n,ex_v):

		if len(ex_n) & len(ex_v) > 0:

			self.changed_values_dic[ex_n] = int(ex_v)
			self.ids.test.text = str(ex_n)
			self.ids.f_expense_input.text = ''
			self.ids.f_expense_v_input.text = ''

	def clear_all(self):

		self.ids.dic_values_wrap.clear_widgets()

	def show_edits(self):

		self.clear_all()

		for i in self.changed_values_dic:
			self.ids.dic_values_wrap.add_widget(Label(text='{} {}'.format(i, self.changed_values_dic[i]),color=(1,1,1,1)))

	def send_request(self):

		search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
		# print search_url
		self.request = UrlRequest(search_url, self.populate,on_error=self.on_error,on_failure=self.on_failure) # <2>

	def on_error(self,request,*args):

		# print (args)
		print ('on error {}'.format(request.result))

	def on_failure(self,request,*args):

		# print (args)
		print ('on failure {}'.format(request.result))

	def populate(self,request,*args):

		# print'entered populate'v
		l = []
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
		# print ('{}'.format(conv_eur))
		dol = l[deda]
		conv_dol = str(dol)
		default_setup_dic = {'porez': 22400,
				'stan': float(eur) * 225,
				'osiguranje': 3000,
				'kuca': 20000,
				'racuni': 10000,}

		if self.store.get('flag')['value'] == 'False':
			for key in default_setup_dic:
				self.changed_values_dic[key] = default_setup_dic[key]




		# exp_sum = sum(expenses_values.values())
		# print(self.changed_values_dic.values())
		exp_sum = sum(self.changed_values_dic.values())
		pay_sum = float(float(dol) * 1350)
		left_sum = float(float(dol) * 1350) - float(exp_sum)

		self.ids.avg_rate_dol_value.text = str(conv_dol)
		self.ids.avg_rate_eur_value.text = str(conv_eur)
		self.ids.paycheck_value.text = str(pay_sum)
		self.ids.expenses_value.text = str(exp_sum)
		self.ids.clean_leftover_value.text = str(left_sum)

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

		MainView.store['flag'] = {'value':'False'}
		print(MainView.store.get('flag'))

	def _update_clock(self, dt):

		self.time = time()

	def show_popup(self):

		p = CustomPopup()
		p.ids.mode_state.text = str(MainView.store.get('flag')['value'])
		print(MainView.store.get('flag'))

		if MainView.store.get('flag')['value'] == 'True':
			p.ids.default_setup.active = True

		print(p.ids.default_setup.active)
		p.open()
	pass

if __name__ == '__main__':

	PaycheckApp().run()







