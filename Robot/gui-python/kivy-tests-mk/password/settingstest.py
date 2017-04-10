import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.settings import SettingString
from kivy.uix.label import Label


class PasswordLabel(Label):
	pass


root = Builder.load_string('''
<SettingPassword>:
	PasswordLabel:
		text: '(set)' if root.value else '(unset)'
		pos: root.pos
		font_size: '15sp'
Button:
	on_release: app.open_settings()
''')


class SettingPassword(SettingString):
	def _create_popup(self, instance):
		super(SettingPassword, self)._create_popup(instance)
		self.textinput.password = True

	def add_widget(self, widget, *largs):
		if self.content is None:
			super(SettingString, self).add_widget(widget, *largs)
		if isinstance(widget, PasswordLabel):
			return self.content.add_widget(widget, *largs)

class TestApp(App):
	def build(self):
		return root

	def build_config(self, config):
		config.setdefaults('test', {'pw': ''})
		print 'pw:', config.get('test', 'pw')

	def build_settings(self, settings):
		settings.register_type('password', SettingPassword)
		settings.add_json_panel('Settings', self.config, filename='settings.json')

if __name__ == '__main__':
	TestApp().run()