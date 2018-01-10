from time import time

import kivy
from kivy.app import App
from kivy.modules.console import Console, ConsoleAddon, ConsoleLabel
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, NumericProperty, Clock, ListProperty, \
    partial, Logger
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')

class ConsoleAddonFps(ConsoleAddon):
    def init(self):
        self.lbl = ConsoleLabel(text="0 Fps")
        self.console.add_toolbar_widget(self.lbl, right=True)

    def activate(self):
        self.event = Clock.schedule_interval(self.update_fps, 1 / 2.)

    def deactivated(self):
        self.event.cancel()

    def update_fps(self, *args):
        fps = Clock.get_fps()
        self.lbl.text = "{} Fps".format(int(fps))

Console.register_addon(ConsoleAddonFps)

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


class Mo(ModalView):

    pass

class StyleLabel(BoxLayout):
    def remove_single_show(self,te):
        MainView().dic_store.delete(te)
        self.clear_widgets()

    pass

class SettingsButton(BoxLayout):
    pass

class HiddenButton(BoxLayout):
    hid_flag_obj = ObjectProperty()
    def __init__(self, **kwargs):
        super(HiddenButton, self).__init__(**kwargs)

        if MainView.store.exists('hidden'):
            if MainView.store['hidden']['value']:
                # print('show exists')
                Clock.schedule_once(partial(self.set_visible,'1'), 3)
            else:
                # print('hide exists')

                Clock.schedule_once(partial(self.set_visible,'0'), 3)
        else:
            Clock.schedule_once(partial(self.set_visible,'0'), 3)
            # print('hide no')

    def set_visible(self,v,*args):
        # print('Opacity from set visible {}'.format(self.ids.hidden_b.opacity))
        # print(v)
        self.ids.hidden_b.opacity = v

    def on_touch_down(self, touch):

        if touch.is_triple_tap:
            self.hidden_feature_enable()
        if touch.is_double_tap:
            self.hidden_feature_disable()

    def hidden_feature_enable(self,*args):
        self.ids.hidden_b.opacity = 1
        MainView.store['hidden'] = {'value':True}

    def hidden_feature_disable(self,*args):
        self.ids.hidden_b.opacity = 0
        MainView.store['hidden'] = {'value':False}

    pass

class CustomPopup(Popup):

    mode = ObjectProperty()

# Dispatch event on_active checkbox to Popup ModeState label & update store JSON value
    def set_flag_edit(self,instance,value):

        # print(value)
        MainView.store['flag_add_edit'] = {'value':value}
        print(value)
        if value:
            mv = MainView()
            print(mv.ids)
            mv.ids.info.text = 'Enable Add/Edit'
            mv.ids.info.color = kivy.utils.get_color_from_hex('#FFFFFF')



    def set_flag_clean(self,instance,value):
        MainView.store['flag_clean'] = {'value':value}
        # print(value)

        if value:
            self.ids.paycheck_amount_clean.opacity= .9
            self.ids.paycheck_amount_clean.readonly = False
            self.ids.update_paycheck_amount.opacity = .9
            # self.ids.paycheck_amount_clean.focus = True
            MainView.changed_values_dic = {}
        else:
            self.ids.paycheck_amount_clean.opacity = 0
            # self.ids.paycheck_amount_clean.readonly = True
            self.ids.update_paycheck_amount.opacity = 0
            MainView.store['paycheck_amount'] = {'value': MainView.store['init_paycheck_amount']['value']}

    def set_paycheck_amount_clean(self,pay_amount,state):
        if state:
            if len(pay_amount) > 1:
                MainView.store['paycheck_amount'] = {'value': int(pay_amount)}
                self.ids.paycheck_amount_clean.text = ''
                self.ids.paycheck_amount_clean.hint_text = ''

            else:
                self.ids.paycheck_amount_clean.hint_text = 'invalid amount'

    def on_open(self):
        if MainView.store.exists('flag_clean'):
            if MainView.store['flag_clean']['value']:
                self.ids.paycheck_amount_clean.focus = 'True'
    pass

class MainView(BoxLayout):

# Storing current value for edit mode True Fals. Initialy populated by on start with False.
# Updated  with Custom Popup set_flag_edit event dispatch
    store = JsonStore('edit_mode.json')
    dic_store = JsonStore('expenses.json')
    avg_rates_list = ListProperty()
    avg_rates_list_converted = ListProperty()
    removal = ObjectProperty()
    temp_dic = {}
    hidden_setup_dic = {}
    if store.exists('rates'):

        hidden_setup_dic = {'porez'     : 24364,
                                    'stan'      : float(store['rates']['eur']) * 225,
                                    'osiguranje': 6000,
                                    'kuca'      : 20000,
                                    'racuni'    : 10000, }

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)

        hid_bu = HiddenButton()
        sett_bu = SettingsButton()
        if self.store.exists('init_paycheck_amount'):
            self.remove_login()

        self.ids.nav.add_widget(hid_bu)
        self.ids.nav.add_widget(sett_bu)

# Show
    def keyboard_shrink(self):
        self.ids.im.size_hint_y = '.5'

# Remove Initial App screen by calling RemoveLogin() after setting init paycheck amount and storing in MainView Store Json Store
    def remove(self,init_am_v):
        if len(init_am_v)>1:
            self.remove_login()
            MainView.store['paycheck_amount'] = {'value': int(init_am_v)}
            MainView.store['init_paycheck_amount'] = {'value': int(init_am_v)}
            # print(self.children)
        else:
            self.ids.init_s_input.hint_text='Wrong Value!'

# Methon for removing Init App screen Widget from Curent View
# Updating Main View Widget to full size and opacity
    def remove_login(self):

        self.remove_widget(self.ids.init_s)
        self.ids.main_v.size_hint_y = 1
        self.ids.main_v.opacity = 1

    def set_currency_flag(self,va):
        # print(va)
        if va:

            self.ids.f_expense_v_input.background_color = [.2, .8, .8, .8]
            self.ids.f_expense_v_input.hint_text = 'EUR'
            self.ids.f_expense_v_input.hint_text_color =  [1, 1, 1, 1]
        else:

            self.ids.f_expense_v_input.background_color = [1, 1, 1, 1]
            self.ids.f_expense_v_input.hint_text_color = [0.5, 0.5, 0.5, 1.0]
            self.ids.f_expense_v_input.hint_text = 'Amount'
        MainView.store['currency_ex_v'] = {'value': va}

# Event dispatched  triggered on Save button clicked
# First arg taken from Input Expanse Name , second arg taken from Input Expense Amount
# Adding values to Main View Expenses Json store EX_N as key and pair "value: EX_V"
# Save action checks if Flag Add/Edit is True in order to proceed, if not warns user with input / label text change
# Callback Show_Edits
    def save_entry(self,ex_n,ex_v):
        # print(len(ex_n))
        # print(len(ex_v))

        if self.store.exists('flag_add_edit'):

            if self.store['flag_add_edit']['value']:

                if len(ex_n) > 0:
                    if len(ex_v) > 0:

                        if self.store.exists('currency_ex_v'):

                            if self.store['currency_ex_v']['value']:
                                self.dic_store.put(ex_n, value=int(ex_v)*float(self.store['rates']['eur']))
                                # print('done with eur')
                            else:
                                self.dic_store.put(ex_n, value=int(ex_v))
                        self.ids.test.text = str(ex_n)
                        Clock.schedule_once(partial(self.update_exp_fields, 'Name','Amount'), 0.3)
                        self.show_edits()
                else:
                    # print(len(ex_n))
                    # print(len(ex_v))
                    self.update_exp_fields('Non valid !', 'Non valid !')
            else:
                self.ids.info.text = 'Enable Expense Add / Edit'
                self.ids.info.color = kivy.utils.get_color_from_hex('#ff0000')
                self.update_exp_fields('Name', 'Amount')
        else:
            return FileExistsError

# Updating expenses input field to be clear after successfull Save_Entry. Args predifined in Save_Entry call
    def update_exp_fields(self,name,amount,*args):

        self.ids.f_expense_input.text = ''
        self.ids.f_expense_input.hint_text = name
        self.ids.f_expense_v_input.text = ''
        self.ids.f_expense_v_input.hint_text = amount
        # self.ids.currency_lab_hidden.opacity = 0
        self.ids.eur_set_value.active = False
        MainView.store['currency_ex_v'] = {'value': False}


# Clear all labels from Widget displaying Expenses dict values added by Show_Edits as Label widget
    def clear_all(self):
        # hack: lis must be used because of Runtime Error in case of iterating over mutable dic values and removing them
        lis = list(self.dic_store.keys())
        self.ids.dic_values_wrap.clear_widgets()

        for i in lis:
            # print('deleting {}'.format(i))
            self.dic_store.delete(i)
        self.temp_dic = {}


# Add iterated values from Dic Store Expenses Json Store to temp_dic
# Adding labels Class StyleLabel by iterating through temp_dic
# Clearing previously added Label widget by self
# Settings label text and color

    def show_edits(self,*args):
        self.ids.dic_values_wrap.clear_widgets()
        # print(self)
        self.populate_temp_dic()
        # print(self.temp_dic)
        # print('>>>>>>>>>>>>>>>')
        self.ids.dic_values_wrap.clear_widgets()
        for key in self.temp_dic:
            # print('{} {}'.format(key,self.temp_dic[key]))
            k = StyleLabel()
            self.ids.dic_values_wrap.add_widget(k)
            k.ids.exp_show_single.text = '{} : {}'.format(key, self.temp_dic[key])
            k.ids.rem_exp_show_single.text = '{}'.format(key)
            # print('{} {}'.format(key, self.temp_dic[key]))
            # print(k.ids.exp_show_single.text)

# Get data from url, event triggered by on_click GET button

    def send_request(self,*args):
        # print('send request')
        search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
        self.request = UrlRequest(search_url, self.get_avg_rates,on_error=self.on_error,on_failure=self.on_failure,on_progress=self.on_progress) # <2>

    def on_error(self,request,*args):
        # print ('on error {}'.format(request.result))
        return False
    def on_failure(self,request,*args):
        # print ('on failure {}'.format(request.result))
        return False
    def on_progress(request,current_size,total_size,*args):
        # print('Progress {} {}'.format(current_size,total_size))
        return True

# Parse Send_Request request and append HTML tag line content to l list
# Iterate over enumarated list grabing Eur Dol values and assigning to local variable for usage as index of list
# Assigning eur and dol values by passing index from local var to list
# Formating eur and dol values to string for label usage
# Storing eur and dol values to MainView Store Json Store as par values
    def get_avg_rates(self,request,*args):
        l =[]
        baba = None
        deda = None

        anchorStart, anchorEnd = makeHTMLTags("td")
        htmlText = request.result
        anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd
        for tokens, start, end in anchor.scanString(htmlText):
            l.append(tokens.body)

        for i, j in enumerate(l):
            if j == 'EUR':
                baba = i + 2
            if j == 'USD':
                deda = i + 2

        eur = l[baba]
        conv_eur = str(eur)
        dol = l[deda]
        conv_dol = str(dol)

        self.store['rates'] = {'eur': conv_eur, 'dol': conv_dol}


# Arg 1 needs to be EUR value , afterwards parsed from string to float
# Arg 2 needs to be DOL value , afterwards parsed from string to float
# Arg 3 needs to be Dictionary,
# Default paycheck_amount set to 1350
    def calculate(self, stored_eur_rate, stored_dol_rate, expense_in, paycheck_amount):




        exp_sum = round(sum(expense_in.values()), 2)

        # print(exp_sum)
        pay_sum = round((float(stored_dol_rate) * paycheck_amount), 2)
        # print(pay_sum)
        left_sum = round((float(stored_dol_rate) * paycheck_amount) - float(exp_sum), 2)
        # print(left_sum)
        self.content_update(stored_dol_rate, stored_eur_rate, pay_sum, exp_sum, left_sum)

    def content_update(self,st_dol_rate, st_eur_rate, p_sum, e_sum, l_sum):
        self.ids.avg_rate_dol_value.text = str(st_dol_rate)
        self.ids.avg_rate_eur_value.text = str(st_eur_rate)
        self.ids.paycheck_value.text = str(p_sum)
        self.ids.expenses_value.text = str(e_sum)
        self.ids.clean_leftover_value.text = str(l_sum)

    def control_content(self):
        paycheck_amount=None
        if self.store.exists('paycheck_amount'):
            # print('entered if calculation')
            try:
                paycheck_amount = int(self.store['paycheck_amount']['value'])
            except KeyError:
                # print('No current entry for paycheck')
                pass

            if self.store.exists('hidden') & self.store['hidden']['value']:
                # print('set content for hidden')
                self.populate_temp_dic()
                if len(self.temp_dic.keys()) > 0:
                    for key in self.temp_dic:
                        self.hidden_setup_dic[key] = self.temp_dic[key]
                        # print('{} {}'.format(key, self.temp_dic[key]))
                # print(self.hidden_setup_dic)
                self.calculate(self.store['rates']['eur'], self.store['rates']['dol'], self.hidden_setup_dic, paycheck_amount)
            else:
                if self.store.exists('flag_clean') & self.store['flag_clean']['value']:
                    # print('2')
                    self.populate_temp_dic()
                    self.calculate(self.store['rates']['eur'], self.store['rates']['dol'], self.temp_dic, paycheck_amount)

                if self.store.exists('flag_clean') & self.store['flag_clean']['value'] is False:
                    # print('3')
                    self.calculate(self.store['rates']['eur'], self.store['rates']['dol'], {}, paycheck_amount)

                if self.store.exists('flag_clean') & self.store['flag_add_edit']['value'] & self.store['flag_clean']['value'] is False:
                    # print('4')
                    self.populate_temp_dic()
                    self.calculate(self.store['rates']['eur'], self.store['rates']['dol'], self.temp_dic, paycheck_amount)

    def populate_temp_dic(self):
        self.temp_dic = {}
        for i in self.dic_store.keys():
            # print(i)
            self.temp_dic[i] = self.dic_store[i]['value']

    def show_tip(self):
        Mo().open(self)

class PaycheckApp(App):
    time = NumericProperty(0)
    flags_dic = {
        'flag_add_edit':False,
        'flag_clean': False,
        'paycheck_amount': 1350,
        'hidden': False,
        'expenses': {},
        'rates': None
    }

    def build(self):

        Clock.schedule_interval(self._update_clock, 1 / 60.)
        root = BoxLayout(orientation='vertical')
        root.add_widget(MainView())
        return root

    def on_pause(self):

        return True

    def on_start(self):
        mv = MainView()
# Set initial value of FALSE to Main View store and Values for eur dol
        if MainView.store.exists('init_paycheck_amount'):
            MainView().ids.init_s.size_hint_y = 0
        self.setup_flag(self.flags_dic)
        Clock.schedule_once(partial(mv.send_request, 'self'), 1)

    def setup_flag(self,dic):
        for i in dic:
            if not MainView.store.exists(str(i)):
                MainView.store[str(i)] = {'value':dic[i]}
                # print('Setting up : {} {}'.format(i,dic[i]))

    def _update_clock(self, dt):

        self.time = time()

    def show_popup(self):

        p = CustomPopup()
# Set initial Label value from store json. Updated Label on Popup open with latest value in store JSON
# 		p.ids.mode_state.text = str(MainView.store.get('flag_add_edit')['value'])
# Set Checkbox value on Popup open , value taken from store JSON
        if MainView.store['flag_add_edit']['value']:
            p.mode_edit.active = True
        if MainView.store['flag_clean']['value']:
            p.mode_clean.active = True
        p.ids.paycheck_amount_clean.hint_text = str(MainView.store['paycheck_amount']['value'])
        p.open()
    pass

if __name__ == '__main__':

    PaycheckApp().run()






