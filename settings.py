#A class to store the settings
class Settings():
	def __init__(self):
		#initialize the game's static settings
		#screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#ship settings	
		self.ship_speed_factor = 1.5
		self.ship_limit = 3

		#bullet settings
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60,60,60
		self.bullets_allowed = 5

		#alien settings
		self.alien_speed_factor = 10
		self.fleet_drop_speed = 10
		#fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

		#how quickly the game speeds up
		self.speedup_scale = 15
		#how quickly the alien point values increase
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		#Initialize settings that change throughout the game.
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1.5
		#fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

		#scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points*self.score_scale)
		print(self.alien_points)
