import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.cache import Cache
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.modules.console import Console, ConsoleAddon, ConsoleLabel
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, NumericProperty, Clock, ListProperty, \
    partial, Logger
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.video import Video
from pyparsing import makeHTMLTags, SkipTo
from datetime import datetime as datetime
from time import time

kivy.require('1.9.1')

class ScrollContainer(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollContainer, self).__init__(**kwargs)
        Logger.info('ScrollContainer: initialized')
        sc = ScrollGrid()
        sc.width = self.width - 25
        self.add_widget(sc)


class ScrollGrid(GridLayout):

    def __init__(self, **kwargs):
        super(ScrollGrid, self).__init__(**kwargs)
        self.clear_widgets()
        Logger.info('ScrollGrid: clearing previos widgets')
        self.bind(minimum_height=self.setter('height'))
        scroll_grid_dic = {}
        Logger.info('ScrollGrid: Empty dic to fill {} '.format(scroll_grid_dic))
        is_expenses_dict_empty = len(MainView.dic_store.keys())
        Logger.info('ScrollGrid: Check if dic is empty {}'.format(is_expenses_dict_empty))

        if is_expenses_dict_empty > 0:
            Logger.info('ScrollGrid: Injecting expenses')
            for i in MainView.dic_store.keys():
                Logger.info('ScrollGrid: scroll grid loop key{}'.format(i))
                scroll_grid_dic[i] = '{} {}'.format(MainView.dic_store[i]['value'],
                                                    MainView.dic_store[i]['currency'])
        else:
            Logger.info('ScrollGrid: No expenses in MainView.dic_store_keys')
            scroll_grid_dic = {}

        for key in scroll_grid_dic:
            Logger.info('ScrollGrid: add exp label key {} {}'.format(key, scroll_grid_dic[key]))
            k = StyleLabel()
            self.add_widget(k)

            k.ids.exp_show_single.text = '{} : {}'.format(key, scroll_grid_dic[key])
            Logger.info('ScrollGrid: Label added {} {}'.format(key, scroll_grid_dic[key]))
            k.ids.rem_exp_show_single.text = '{}'.format(key)
            Logger.info('ScrollGrid: Remove button added {}'.format(key))
            k.ids.show_single_mo.text = '{}'.format(scroll_grid_dic[key])
            Logger.info('ScrollGrid: Modal open button added {}'.format(scroll_grid_dic[key]))



class Mo(ModalView):
    gif_wrap = ObjectProperty()

    def __init__(self, **kwargs):
        super(Mo, self).__init__(**kwargs)
        Logger.info('Mo: children {}'.format(self.gif_wrap.children))

        if len(self.gif_wrap.children) < 1:
            xxx = Cache.get('movid', 'vid')
            xxx.state = 'play'
            xxx.volume = 0
            # xxx.anim_delay = 0
            self.gif_wrap.add_widget(xxx)

    def re(self):
        Logger.info('Mo: clear tip Modal {}'.format(self.ids))
        self.gif_wrap.clear_widgets()
        Logger.info('Mo: clear tip Modal after {}'.format(self.ids))


class ExpModal(ModalView):
    def __init__(self, **kwargs):
        super(ExpModal, self).__init__(**kwargs)
        Logger.info('ExpModal: children {}'.format(self.children))

    pass


class StyleLabel(BoxLayout):
    converted_exp_str_one = ''
    converted_exp_str_two = ''
    now = datetime.now()

    def remove_single_show(self, te):
        Logger.info('StyleLabel: remove expense {}'.format(te))
        MainView.dic_store.delete(te)
        self.clear_widgets()

    def exp_converter(self, string_to_parse):
        parsed_cur = string_to_parse[-3:]
        parse_val = float(string_to_parse[:-4])
        eur_c = float(MainView.store['rates']['eur'])
        dol_c = float(MainView.store['rates']['dol'])
        Logger.info('StyleLabel: expense currency for conversion {}'.format(parsed_cur))

        if parsed_cur == 'RSD':
            Logger.info('StyleLabel-exp_converter: converting from {}'.format(parsed_cur))
            to_dol = parse_val / dol_c
            to_eur = parse_val / eur_c
            self.converted_exp_str_one = '{} {} = {} USD'.format(parse_val, parsed_cur, round(to_dol, 2))
            self.converted_exp_str_two = '{} {} = {} EUR'.format(parse_val, parsed_cur, round(to_eur, 2))

        elif parsed_cur == 'USD':
            Logger.info('StyleLabel-exp_converter: converting from {}'.format(parsed_cur))
            to_rsd = parse_val * dol_c
            to_eur = parse_val * (dol_c / eur_c)
            self.converted_exp_str_one = '{} {} = {} RSD'.format(parse_val, parsed_cur, round(to_rsd, 2))
            self.converted_exp_str_two = '{} {} = {} EUR'.format(parse_val, parsed_cur, round(to_eur, 2))
        else:
            Logger.info('exp_converter: converting from {}'.format(parsed_cur))
            to_rsd = parse_val * eur_c
            to_dol = parse_val * (eur_c / dol_c)
            self.converted_exp_str_one = '{} {} = {} RSD'.format(parse_val, parsed_cur, round(to_rsd, 2))
            self.converted_exp_str_two = '{} {} = {} USD'.format(parse_val, parsed_cur, round(to_dol, 2))

    def open_modal(self, tex):
        Logger.info('StyleLabel-open_modal: children {}'.format(self.children))
        exp_m = ExpModal()
        exp_m.open(self)

        colo = kivy.utils.get_color_from_hex('#31ddd0')

        self.exp_converter(tex)
        Logger.info('StyleLabel-open_modal: first converted currency {}'.format(self.converted_exp_str_one))
        Logger.info('StyleLabel-open_modal: first converted currency {}'.format(self.converted_exp_str_two))
        exp_m.ids.cur_converted_one.text = self.converted_exp_str_one
        exp_m.ids.cur_converted_one.color = colo
        exp_m.ids.cur_converted_two.text = self.converted_exp_str_two
        exp_m.ids.cur_converted_two.color = colo
        exp_m.ids.conv_date.text = self.now.strftime("%Y-%m-%d")
        exp_m.ids.conv_date.color = colo

    pass


class SettingsButton(BoxLayout):

    pass


class CustomPopup(Popup):

    mode = ObjectProperty()
    settings_currency_check_rsd = ObjectProperty()
    settings_currency_check_dol = ObjectProperty()
    settings_currency_check_eur = ObjectProperty()

    # Dispatch event on_active checkbox to Popup ModeState label & update store JSON value
    def flag_clean_content_visible(self):
        Logger.info('CustomPopup: Set popup content visible')

        self.ids.settings_content_wrap.opacity = .9
        self.ids.settings_content_wrap.disabled = False

    def flag_clean_content_hidden(self):
        Logger.info('CustomPopup: Set popup content visible')

        self.ids.settings_content_wrap.opacity = 0
        self.ids.settings_content_wrap.disabled = True

    def set_flag_clean(self, instance, value):

        MainView.store['flag_clean'] = {'value': value}

        if value:
            self.flag_clean_content_visible()
            MainView.changed_values_dic = {}
        else:
            self.flag_clean_content_hidden()
            MainView.store['paycheck_amount'] = {'value': MainView.store['init_paycheck_amount']['value']}

    def settings_store(self, value, store_key):

        MainView.store['paycheck_amount'] = {'value': float(value)}
        MainView.store['init_paycheck_amount'] = {'value': float(value)}
        MainView.store['paycheck_amount_currency'] = {'value': store_key}
        Logger.info('CustomPopup: New value to set {} {}'.format(value,store_key))

        self.ids.paycheck_amount_clean.text = ''
        self.ids.paycheck_amount_clean.hint_text = '{} {}'.format(value, store_key)

    def set_paycheck_amount_clean(self, pay_amount, state):

        if state:
            if len(pay_amount) > 1:
                if self.settings_currency_check_rsd.active:
                    self.settings_store(pay_amount, 'RSD')
                    Logger.info('CustomPopup: set paycheck to {} rsd '.format(pay_amount))


                elif self.settings_currency_check_dol.active:
                    self.settings_store(pay_amount, 'USD')
                    Logger.info('CustomPopup: set paycheck to {} usd '.format(pay_amount))

                else:
                    self.settings_store(pay_amount, 'EUR')
                    Logger.info('CustomPopup: set paycheck to {} eur '.format(pay_amount))

            else:
                self.ids.paycheck_amount_clean.hint_text = 'invalid amount'
                Logger.info('CustomPopup: amount not valid {} '.format(len(pay_amount)))

    def on_open(self):
        Logger.info('CustomPopup: Open')
        if MainView.store.exists('flag_clean'):
            if MainView.store['flag_clean']['value']:
                self.ids.paycheck_amount_clean.focus = 'True'
                self.flag_clean_content_visible()
            else:
                self.flag_clean_content_hidden()

    pass


# class CarouselNav(BoxLayout):
#     def __init__(self, **kwargs):
#         super(CarouselNav, self).__init__(**kwargs)
#
#     def next_slide(self):
#         sl = MainView()
#         # print(MainView.main_v_carousel_view.current_slide)
#         # MainView().main_v_carousel_view.index = 2
#         print(sl.ids.carousel_view.current_slide.ids)
#         # MainView().ids.carousel_view.load_next()
#     def prev_slide(self):
#         sl = MainView()
#         # print(MainView.main_v_carousel_view.current_slide)
#         # MainView().main_v_carousel_view.current_slide = 1
#         print(sl.ids.carousel_view.load_previous())
#         # MainView().ids.carousel_view.load_previous()
#     pass
class MainView(BoxLayout):

    # Storing current value for edit mode True Fals. Initialy populated by on start with False.
    # Updated  with Custom Popup set_flag_edit event dispatch
    now = datetime.now()

    store = JsonStore('edit_mode.json')
    dic_store = JsonStore('expenses.json')
    avg_rates_list = ListProperty()
    avg_rates_list_converted = ListProperty()
    removal = ObjectProperty()
    temp_dic = {}
    expense_currency_check_rsd = ObjectProperty()
    expense_currency_check_dol = ObjectProperty()
    expense_currency_check_eur = ObjectProperty()
    average_rate_dolar_label = ObjectProperty()
    average_rate_dolar_value_label = ObjectProperty()
    average_rate_euro_label = ObjectProperty()
    average_rate_euro_value_label = ObjectProperty()
    paycheck_label = ObjectProperty()
    paycheck_value_label = ObjectProperty()
    expenses_label = ObjectProperty()
    expense_value_label = ObjectProperty()
    clean_leftover_label = ObjectProperty()
    clean_leftover_value_label = ObjectProperty()
    main_v_carousel_view = ObjectProperty()
    first_check_slide = ObjectProperty()
    second_check_slide = ObjectProperty()
    init_s_im = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        Logger.info('MainView: Initialized {}'.format(self))

        self.setup_inits()
        self.setup_nav_settings_button()
        Logger.info('MainView: Settings button added {}'.format(True))

        # self.ids.foot_nav.add_widget(fonav)
    def setup_inits(self):
        if self.store.exists('init_paycheck_amount'):
            Logger.info('MainView: Init screen removed {}'.format(True))
            self.remove_login()
        else:
            self.inits_anim(self.init_s_im)
    def setup_nav_settings_button(self):
        if len(self.ids.nav.children) < 1:
            print(self.ids.nav.children)
            sett_bu = SettingsButton()
            print(self.ids.nav)
            self.ids.nav.add_widget(sett_bu)
            Logger.info('MainView: Settings button added {}'.format(True))
        else:
            print(2)
            Logger.info('MainView: Settings button does not to be added {}'.format(True))

    # Show
    def inits_anim(self, im):
        Logger.info('MainView: Animation started {}'.format(im))

        # print('x {}'.format(im.pos[0]))
        Logger.info('MainView: Img pos arg x '.format(im.pos[0]))

        # print('y {}'.format(im.pos[1]))
        Logger.info('MainView: Img pos arg y '.format(im.pos[1]))

        # print(self.to_widget(self.width,self.height))
        animation = Animation(x=330, y=400, duration=4, t='out_bounce') + Animation(x=330, y=20, duration=4,
                                                                                    t='out_elastic')
        animation.repeat = True
        animation.start(im)

    def keyboard_shrink(self):
        # self.init_s_im.size_hint_y = '.5'
        # print('no')
        pass

    def prim(self, ind):
        if ind is 0:
            Logger.info('MainView: Slide set to Main {}'.format(ind))

            self.first_check_slide.active = True
            self.second_check_slide.active = False
            self.prev_slide()

        else:
            Logger.info('MainView: Slide set to Exo {}'.format(ind))

            self.second_check_slide.active = True
            self.first_check_slide.active = False
            self.next_slide()
        # print(self.main_v_carousel_view.index)

    def prev_slide(self):
        #         sl = MainView()
        # print('prev {}'.format(self.main_v_carousel_view.index))
        Logger.info('MainView: Set slide prev ind {}'.format(self.main_v_carousel_view.index))

        self.main_v_carousel_view.load_previous()

    def next_slide(self):
        #         sl = MainView()
        # print('next {}'.format(self.main_v_carousel_view.index))
        Logger.info('MainView: Set slide next ind {}'.format(self.main_v_carousel_view.index))

        self.main_v_carousel_view.load_next()
        #         # MainView().main_v_carousel_view.index = 2
        #         print(sl.ids.carousel_view.current_slide.ids)
        #         # MainView().ids.carousel_view.load_next()

    # Remove Initial App screen by calling RemoveLogin() after setting init paycheck amount and storing in MainView Store Json Store
    def initial_s_store(self, value, store_key):
        Logger.info('MainView: InitScreen: Store pay amount {} curr {}'.format(value, store_key))

        self.store['paycheck_amount'] = {'value': float(value)}
        self.store['init_paycheck_amount'] = {'value': float(value)}
        self.store['paycheck_amount_currency'] = {'value': store_key}

    def remove(self, init_am_v):

        if len(init_am_v) > 1:

            if self.ids.rsd_pick.active:
                # print('set rsd')

                # print(init_am_v)

                self.initial_s_store(init_am_v, self.ids.rsd_lab.text)

            elif self.ids.dol_pick.active:
                # print('set dol')

                # print(init_am_v)

                self.initial_s_store(init_am_v, self.ids.dol_lab.text)

            else:
                # print('set eur')

                # print(init_am_v)

                self.initial_s_store(init_am_v, self.ids.eur_lab.text)

            self.remove_login()
            # print(self.children)
        else:
            self.ids.init_s_input.hint_text = 'Wrong Value!'
            # print(self.ids.rsd_pick.active)
            # print(self.ids.eur_pick.active)
            # print(self.ids.dol_pick.active)

    # Methon for removing Init App screen Widget from Curent View
    # Updating Main View Widget to full size and opacity
    def remove_login(self):

        self.remove_widget(self.ids.init_s)
        self.ids.main_v.size_hint_y = 1
        self.ids.main_v.opacity = 1

    def set_currency_flag(self, va):
        # print(va)
        if va:

            self.ids.f_expense_v_input.background_color = [.2, .8, .8, .8]
            self.ids.f_expense_v_input.hint_text = 'EUR'
            self.ids.f_expense_v_input.hint_text_color = [1, 1, 1, 1]
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
    def store_expense_with_currency(self, ex_name, ex_value, ex_currency):
        Logger.info(
            'MainView: Storing expense currnency: name {} value {} curr {}'.format(ex_name, ex_value, ex_currency))

        self.dic_store.put(ex_name, value=int(ex_value), currency=ex_currency)

    def save_entry(self, ex_n, ex_v):
        # print(len(ex_n))
        # print(len(ex_v))
        # print(len(ex_n)>0)
        # print(len(ex_v)>0)

        if (len(ex_n) > 0) and (len(ex_v) > 0):
            # print('first if')
            if self.expense_currency_check_rsd.active:
                self.store_expense_with_currency(ex_n, ex_v, 'RSD')
                # print('saving expense rsd {} {} '.format(ex_n,ex_v))

            elif self.expense_currency_check_dol.active:
                self.store_expense_with_currency(ex_n, ex_v, 'USD')
                # print('saving expense dol {} {} '.format(ex_n, ex_v))
            else:
                self.store_expense_with_currency(ex_n, ex_v, 'EUR')
                # print('saving expense eur {} {} '.format(ex_n, ex_v))

            Clock.schedule_once(partial(self.update_exp_fields, 'Name', 'Amount'), 0.3)
            self.show_edits()
        else:
            # print('fail')
            # print(len(ex_n))
            # print(len(ex_v))
            self.update_exp_fields('Non valid !', 'Non valid !')

    # Updating expenses input field to be clear after successfull Save_Entry. Args predifined in Save_Entry call
    def update_exp_fields(self, name, amount, *args):

        self.ids.f_expense_input.text = ''
        self.ids.f_expense_input.hint_text = name
        self.ids.f_expense_v_input.text = ''
        self.ids.f_expense_v_input.hint_text = amount
        # self.ids.currency_lab_hidden.opacity = 0

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

    def show_edits(self, *args):
        self.ids.dic_values_wrap.clear_widgets()
        # print(self)
        # self.populate_temp_dic()
        # print(self.temp_dic)
        # print('>>>>>>>>>>>>>>>')
        # self.ids.dic_values_wrap.clear_widgets()

        # for key in self.temp_dic:
        #     print('this is from main {} {}'.format(key, self.temp_dic[key]))
        # print('crazy {}'.format(MainView.temp_dic))
        scroll_cont = ScrollContainer()
        scroll_cont.height = self.ids.dic_values_wrap.height
        self.ids.dic_values_wrap.add_widget(scroll_cont)
        # for key in self.temp_dic:
        #     # print('{} {}'.format(key,self.temp_dic[key]))
        #     k = StyleLabel()
        #     self.ids.dic_values_wrap.add_widget(k)
        #     k.ids.exp_show_single.text = '{} : {}'.format(key, self.temp_dic[key])
        #     k.ids.rem_exp_show_single.text = '{}'.format(key)
        #     # print('{} {}'.format(key, self.temp_dic[key]))
        #     # print(k.ids.exp_show_single.text)

    # Get data from url, event triggered by on_click GET button

    def send_request(self, *args):
        # print('send request')
        search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
        self.request = UrlRequest(search_url, self.get_avg_rates, on_error=self.on_error,
                                  on_failure=self.on_failure, on_progress=self.on_progress)  # <2>

    def on_error(self, request, *args):
        # print ('on error {}'.format(request.result))
        return False

    def on_failure(self, request, *args):
        # print ('on failure {}'.format(request.result))
        return False

    def on_progress(request, current_size, total_size, *args):
        # print('Progress {} {}'.format(current_size,total_size))
        return True

    # Parse Send_Request request and append HTML tag line content to l list
    # Iterate over enumarated list grabing Eur Dol values and assigning to local variable for usage as index of list
    # Assigning eur and dol values by passing index from local var to list
    # Formating eur and dol values to string for label usage
    # Storing eur and dol values to MainView Store Json Store as par values
    def get_avg_rates(self, request, *args):
        l = []
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

        # print('exp {}'.format(exp_sum))
        if self.store['paycheck_amount_currency']['value'] == 'RSD':
            pay_sum = round(paycheck_amount, 2)
        elif self.store['paycheck_amount_currency']['value'] == 'USD':
            pay_sum = round((float(stored_dol_rate) * paycheck_amount), 2)
        else:
            pay_sum = round((float(stored_eur_rate) * paycheck_amount), 2)

        # print(pay_sum)
        left_sum = round(pay_sum - float(exp_sum), 2)
        # print(left_sum)
        self.content_update(stored_dol_rate, stored_eur_rate, pay_sum, exp_sum, left_sum)

    def content_update(self, st_dol_rate, st_eur_rate, p_sum, e_sum, l_sum):
        self.average_rate_dolar_value_label.text = str(st_dol_rate)
        self.average_rate_dolar_label.text = 'USD Avg Rate on {}'.format(self.now.strftime("%Y-%m-%d"))
        self.average_rate_euro_value_label.text = str(st_eur_rate)
        self.average_rate_euro_label.text = 'EUR Avg Rate on {}'.format(self.now.strftime("%Y-%m-%d"))
        self.paycheck_value_label.text = str(p_sum)
        self.expense_value_label.text = str(e_sum)
        self.clean_leftover_value_label.text = str(l_sum)

    def control_content(self):
        paycheck_amount = None
        if self.store.exists('paycheck_amount'):
            # print('entered if calculation')
            try:
                paycheck_amount = self.store['paycheck_amount']['value']
            except KeyError:
                # print('No current entry for paycheck')
                pass

            self.populate_temp_dic()
            self.calculate(self.store['rates']['eur'], self.store['rates']['dol'], self.temp_dic, paycheck_amount)

    def populate_temp_dic(self):
        self.temp_dic = {}
        for i in self.dic_store.keys():
            # print(i)
            if self.dic_store[i]['currency'] == 'RSD':

                self.temp_dic[i] = self.dic_store[i]['value']
            elif self.dic_store[i]['currency'] == 'USD':

                self.temp_dic[i] = (float(self.dic_store[i]['value'])) * (float(self.store['rates']['dol']))
            else:
                self.temp_dic[i] = (float(self.dic_store[i]['value'])) * (float(self.store['rates']['eur']))

    def show_tip(self):
        Mo().open(self)


class PaycheckApp(App):

    time = NumericProperty(0)
    flags_dic = {
        'flag_clean'     : False,
        'paycheck_amount': None,
        'rates'          : None
    }

    def build(self):

        root = BoxLayout(orientation='vertical')
        root.add_widget(MainView())
        return root

    def on_pause(self):

        return True

    def on_start(self):
        mv = MainView()
        # Set initial value of FALSE to Main View store and Values for eur dol
        #         if MainView.store.exists('init_paycheck_amount'):
        #             MainView().ids.init_s.size_hint_y = 0
        self.setup_flag(self.flags_dic)
        Clock.schedule_once(partial(mv.send_request, 'self'), 1)
        Cache.register('movid')
        key = 'vid'
        instance = Video(source='/ani.mp4')
        Cache.append('movid', key, instance)

    def setup_flag(self, dic):
        for i in dic:
            if not MainView.store.exists(str(i)):
                MainView.store[str(i)] = {'value': dic[i]}
                # print('Setting up : {} {}'.format(i,dic[i]))

    def on_stop(self):
        Cache.remove('movid')

    def show_popup(self):

        p = CustomPopup()
        # Set initial Label value from store json. Updated Label on Popup open with latest value in store JSON
        #       p.ids.mode_state.text = str(MainView.store.get('flag_add_edit')['value'])
        # Set Checkbox value on Popup open , value taken from store JSON

        if MainView.store['flag_clean']['value']:
            p.mode_clean.active = True
        p.ids.paycheck_amount_clean.hint_text = str(MainView.store['paycheck_amount']['value'])
        p.open()

    pass


if __name__ == '__main__':
    PaycheckApp().run()

