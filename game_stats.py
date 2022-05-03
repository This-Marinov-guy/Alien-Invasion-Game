#track statistics for Alein Invasion
class GameStats():
	def __init__ (self, ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		#start alien invasion in an inactive state
		self.game_active = False
		#ghigh score should never be reset
		self.high_score = 0

	def reset_stats(self):
		#initialize statistics that can change during the game
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
