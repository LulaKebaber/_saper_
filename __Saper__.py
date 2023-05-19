import random
import math
from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '600')

class SmApp(App):
	def open(self,instance):
		if self.game_state == 'stop' or instance.background_color == (0,1,1,1):
			return
		elif self.flag_on == True and instance.text == '' and self.flag_sum < self.mines_num:
			instance.text = 'Flag'
			self.flag_sum += 1
			i = self.buttons.index(instance)
			if self.value[i] == 0:
				self.flags_on_mines += 1
			if self.flags_on_mines == self.mines_num:
				self.popup_win.open()
			print(self.flags_on_mines)
			return
		elif instance.text == 'Flag' and self.flag_on == True:
			instance.text = ''
			self.flag_sum -= 1
			i = self.buttons.index(instance)
			if self.value[i] == 0:
				self.flags_on_mines -= 1
			print(self.flags_on_mines)
			return
		elif instance.text != '-' and instance.text != 'Flag' and self.flag_on == False:
			i = self.buttons.index(instance)
			if self.value[i] == 0:
				instance.background_normal = 'mine.jpg'
				self.game_state = 'stop'
				self.popup_lose.open()
				print(self.game_state)
			elif self.value[i] == 1:
				instance.background_color = (0,1,1,1)
				instance.text = ''
				self.Found_the_Lake(i)
			else:
				instance.text = str(int(math.log(self.value[i],2)))

	def Found_the_Lake(self,instance):

		self.check_for_someshit(instance)
		for ii in range(len(self.n_around)):
			if self.buttons[self.n_around[ii]].text == 'Flag':
				pass
			elif self.value[self.n_around[ii]] == 1:
				print(self.value)
				self.buttons[self.n_around[ii]].background_color = (0,1,1,1)
				self.buttons[self.n_around[ii]].text = ''
			else:
				self.buttons[self.n_around[ii]].text = str(int(math.log(self.value[self.n_around[ii]],2)))

	def flag_on_fun(self,instance):
		if instance.state == 'down':
			self.flag_on = True
		else:
			print('flag_off')
			self.flag_on = False

	def check_for_someshit(self,instance):
		hor_upper = [i for i in range(1,self.game_width-1)]
		hor_lower = [i for i in range(self.n-self.game_width+1,self.n-1)]
		ver_right = [i for i in range(self.game_width*2-1,self.n-self.game_width,self.game_width)]
		ver_left = [i for i in range(self.game_width,self.n-self.game_width,self.game_width)]

		n1,n2,n3,n4 = 0,self.game_width-1,self.n-self.game_width,self.n-1

		if instance in hor_upper:
			self.n_around = [instance+1,instance-1,instance+self.game_width,instance+self.game_width-1,instance+self.game_width+1]
		elif instance in hor_lower:
			self.n_around = [instance+1,instance-1,instance-self.game_width,instance-self.game_width-1,instance-self.game_width+1]
		elif instance in ver_right:
			self.n_around = [instance-1,instance-self.game_width,instance+self.game_width,instance-self.game_width-1,instance+self.game_width-1]
		elif instance in ver_left:
			self.n_around = [instance+1,instance-self.game_width,instance+self.game_width,instance-self.game_width+1,instance+self.game_width+1]
		else:
			if instance == n1:
				self.n_around = [instance+1,instance+self.game_width,instance+self.game_width+1]
			elif instance == n2:
				self.n_around = [instance-1,instance+self.game_width,instance+self.game_width-1]
			elif instance == n3:
				self.n_around = [instance+1,instance-self.game_width,instance-self.game_width+1]
			elif instance == n4:
				self.n_around = [instance-1,instance-self.game_width,instance-self.game_width-1]
			else:
				self.n_around = [instance-self.game_width-1,instance-self.game_width,instance-self.game_width+1,instance-1,instance+1,instance+self.game_width-1,instance+self.game_width,instance+self.game_width+1]

	def restart(self,instance):
		self.value = []
		self.mines = []
		self.btn_toggle.state = 'normal'
		self.game_state = 'start'
		self.flag_sum = 0
		self.flags_on_mines = 0
		self.flag_on = False
		for i in range(self.n):
			self.buttons[i].text = ''
			self.buttons[i].background_color = (1,1,1,1)
			self.buttons[i].background_normal = 'atlas://data/images/defaulttheme/button'
			self.value.append(1)

		for i in range(self.mines_num):
			self.value[i] = 0
		random.shuffle(self.value)

		for i in range(self.n):
			if self.value[i] == 0:
				self.mines.append(i)

		for i in self.mines:
			self.check_for_someshit(i)
			for ii in range(len(self.n_around)):
				self.value[self.n_around[ii]] *= 2
		print(self.value)

	def create(self,instance):
		#self.sm.current = 'Game'
		self.game_height = int(self.textinput_H.text)
		self.game_width = int(self.textinput_W.text)
		self.mines_num = int(self.textinput_MN.text)
		print(self.game_height,self.game_width)
		self.n = self.game_height * self.game_width
		self.bl = BoxLayout(orientation= 'vertical')
		self.bl2 = BoxLayout(orientation= 'horizontal', size_hint = (1,.2), padding = [150,0,150,0])
		self.gl = GridLayout(cols = self.game_width)

		screen_game = Screen(name = 'Game')
		for i in range(self.n):
			self.buttons.append(Button(text='-', on_press = self.open, font_size = 30))
			self.gl.add_widget(self.buttons[i])

		self.btn_toggle = ToggleButton(size_hint = (.3,1), on_press = self.flag_on_fun, background_normal = 'Flag.png')
		self.bl2.add_widget(self.btn_toggle)
		self.btn_start = Button(size_hint = (.3,1), on_press = self.restart, font_size = 40, text = 'Start')
		self.bl2.add_widget(self.btn_start)
		self.bl.add_widget(self.gl)
		self.bl.add_widget(self.bl2)

		screen_game.add_widget(self.bl)	
		self.sm.add_widget(screen_game)
		self.sm.current = 'Game'

	def build(self):
		self.buttons = []
		self.value = []
		self.mines = []
		self.n_around = []
		self.game_state = ''
		self.flag_on = False
		self.flag_sum = 0
		self.flags_on_mines = 0
		self.popup_lose = Popup(title = 'Your Progress', title_size = '25sp', content = Label(text = 'You Lose!',font_size = 40), size_hint = (None, None), size = (400, 400))
		self.popup_win = Popup(title = 'Your Progress', title_size = '25sp', content = Label(text = 'You win!',font_size = 40), size_hint = (None, None), size = (400, 400))
	#-------------------------------------------------------------

		self.sm = ScreenManager()
		screen_menu = Screen(name = 'Menu')
		self.bl_menu = BoxLayout(orientation= 'vertical', padding = [100,100,100,100], spacing = 20)
		self.textinput_H = TextInput(text = 'Height', multiline = False, font_size = 45)
		self.textinput_W = TextInput(text = 'Width', multiline = False, font_size = 45)
		self.textinput_MN = TextInput(text = 'Mines', multiline = False, font_size = 45)
		self.bl_menu.add_widget(Label(text = 'MineSweeper', font_size = 45))
		self.bl_menu.add_widget(self.textinput_H)
		self.bl_menu.add_widget(self.textinput_W)
		self.bl_menu.add_widget(self.textinput_MN)
		self.bl_menu.add_widget(Button(on_press = self.create, text = 'Start', font_size = 45))
		screen_menu.add_widget(self.bl_menu)
		self.sm.add_widget(screen_menu)


		return self.sm

if __name__ == "__main__":
	SmApp().run()