from time import time
from kivy.app import App
import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, Clock, BooleanProperty, ListProperty, partial
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')


class CustomPopup(Popup):

    mode = ObjectProperty()

# Dispatch event on_active checkbox to Popup ModeState label & update store JSON value
    def set_flag_edit(self,instance,value):

        self.mode.text = str(value)
        MainView.store['flag_edit'] = {'value':'{}'.format(value)}
        print(MainView.store.get('flag'))

    pass

    def set_flag_clean(self,instance,value):
        MainView.store['flag_clean'] = {'value': '{}'.format(value)}
        if value:
            self.ids.paycheck_amount_clean.opacity= .9
            self.ids.paycheck_amount_clean.readonly = False
            self.ids.update_paycheck_amount.opacity = .9
            MainView.changed_values_dic = {}


    def set_paycheck_amount_clean(self,pay_amount,state):
        if state:
            print(pay_amount)
            MainView.store['paycheck_amount'] = {'paycheck': pay_amount}
            self.ids.paycheck_amount_clean.text = ''
            print(state)
            print(MainView.store['paycheck_amount'])
        else:
            MainView.changed_values_dic['paychechk_ammount']=None
            print(MainView.store['paycheck_amount'])

class MainView(BoxLayout):

# Storing current value for edit mode True Fals. Initialy populated by on start with False.
# Updated  with Custom Popup set_flag_edit event dispatch
    store = JsonStore('edit_mode.json')
    avg_rates_list = ListProperty()
    avg_rates_list_converted = ListProperty()
    mode_s = ObjectProperty()

# Disctionary used to calculate final values
    changed_values_dic = DictProperty(None)

# Event dispatched  triggered on Save button clicked
# First arg taken from Input Expanse Name , second arg taken from Input Expense Amount
# Adding values to Main View dic object changed values
# Clearing Input Expense Name and Input Expense Amaount text
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

    def send_request(self,*args):

        search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
        # print search_url
        self.request = UrlRequest(search_url, self.get_avg_rates,on_error=self.on_error,on_failure=self.on_failure,on_progress=self.on_progress) # <2>

    def on_error(self,request,*args):

        # print (args)
        print ('on error {}'.format(request.result))

    def on_failure(self,request,*args):

        # print (args)
        print ('on failure {}'.format(request.result))

    def on_progress(request,current_size,total_size,*args):


        print('Progress {} {}'.format(current_size,total_size))


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
        print()
        if self.store['paycheck_amount']['paycheck']:
            paycheck_amount=int(self.store['paycheck_amount']['paycheck'])
        exp_sum = sum(int(self.changed_values_dic.values()))
        print(exp_sum)
        pay_sum = float(float(stored_dol_rate) * paycheck_amount)
        print(pay_sum)
        left_sum = float(float(stored_dol_rate) * paycheck_amount) - float(exp_sum)
        print(left_sum)


        self.ids.avg_rate_dol_value.text = str(stored_dol_rate)
        self.ids.avg_rate_eur_value.text = str(stored_eur_rate)
        self.ids.paycheck_value.text = str(pay_sum)
        self.ids.expenses_value.text = str(exp_sum)
        self.ids.clean_leftover_value.text = str(left_sum)
    def populate(self):
        print(self.store['rates'])
        self.calculate(self.store['rates']['eur'],self.store['rates']['dol'])
        # print'entered populate'v
        # l = []
        # anchorStart, anchorEnd = makeHTMLTags("td")
        # htmlText = request.result
        # anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd
        #
        # for tokens, start, end in anchor.scanString(htmlText):
        # 	l.append(tokens.body)
        #
        # baba = None
        # deda = None
        #
        # for i, j in enumerate(l):
        # 	if j == 'EUR':
        # 		baba = i + 2
        # 	if j == 'USD':
        # 		deda = i + 2
        # #############################################################
        #
        # # print('{}'.format(l))
        # eur = l[baba]
        # conv_eur = str(eur)
        # # print ('{}'.format(conv_eur))
        # dol = l[deda]
        # conv_dol = str(dol)
        # default_setup_dic = {'porez': 22400,
        # 		'stan': float(eur) * 225,
        # 		'osiguranje': 3000,
        # 		'kuca': 20000,
        # 		'racuni': 10000,}
        #
        # if self.store.get('flag')['value'] == 'False':
        # 	for key in default_setup_dic:
        # 		self.changed_values_dic[key] = default_setup_dic[key]
        #
        #
        #
        #
        # # exp_sum = sum(expenses_values.values())
        # # print(self.changed_values_dic.values())
        # exp_sum = sum(self.changed_values_dic.values())
        # pay_sum = float(float(dol) * 1350)
        # left_sum = float(float(dol) * 1350) - float(exp_sum)
        #
        # self.ids.avg_rate_dol_value.text = str(conv_dol)
        # self.ids.avg_rate_eur_value.text = str(conv_eur)
        # self.ids.paycheck_value.text = str(pay_sum)
        # self.ids.expenses_value.text = str(exp_sum)
        # self.ids.clean_leftover_value.text = str(left_sum)

    def control_content(self):
        a=True
        b= True
        default_setup_dic = {'porez': 22400,
        		'stan': float(self.store['rates']) * 225,
        		'osiguranje': 3000,
        		'kuca': 20000,
        		'racuni': 10000,}

        if a & b:
            print('Should be edit clean mode')
        if a == False & b:
            print('Should be default with adding edit')
            for key in default_setup_dic:
                self.changed_values_dic[key] = default_setup_dic[key]
            # self.changed_values_dic = default_setup_dic




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
        mv = MainView()

        MainView.store['flag'] = {'value':'False'}

        Clock.schedule_once(partial(mv.send_request,'self'), 1)

        print(MainView.store.get('flag'))
        print(MainView.store.get('rates'))


    def _update_clock(self, dt):

        self.time = time()

    def show_popup(self):

        p = CustomPopup()
# Set initial Label value from store json. Updated Label on Popup open with latest value in store JSON
        p.ids.mode_state.text = str(MainView.store.get('flag')['value'])
        print(MainView.store.get('flag'))
# Set Checkbox value on Popup open , value taken from store JSON
        if MainView.store.get('flag')['value'] == 'True':
            p.ids.default_setup.active = True

        print(p.ids.default_setup.active)
        p.open()
    pass

if __name__ == '__main__':

    PaycheckApp().run()







