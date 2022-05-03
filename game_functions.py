import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_fleet_edges(ai_settings, aliens):
	#respond appropriately if any aliens have reached an edge
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	#drop the entire fleet and change the fleet's direction
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1

def check_high_score(stats, sb):
		#check to see if there is a new high score
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			sb.prep_high_score()

def fire_bullet(ai_settings, screen, ship, bullets):
	#Fire a bullet is limit is not reached
	if len(bullets)<ai_settings.bullets_allowed:
		  new_bullet = Bullet(ai_settings, screen, ship)
		  bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	#detetmine the number of aliens that fit in a row
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	#determine the number of rows of aliens that sit on the screen
	available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	#create an alien and place it in a row
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	#create a full fleet of aliens
	#create an alien and find the num of aliens in the row/ spacing between each alien is equal to one alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#create the fleet
	for row_number in range(number_rows):
	   #create the first row of aliens
	   for alien_number in range(number_aliens_x):
		   create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
#respond to keypresses
	if event.key==pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key==pygame.K_LEFT:
		ship.moving_left = True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key==pygame.K_q:
		sys.exit()


def check_keyup_events(event, ship):
#respond to key releases	  
	if event.key==pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key==pygame.K_LEFT:
		ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	#start a new game when the player clicks Play
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#reset the game settings
		ai_settings.initialize_dynamic_settings()
		#hide the mouse cursor
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True

		#reset the sb
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen ,stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event, ship)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	#Update images on the screen and flip to the new screen.
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#draw the score info
	sb.show_score()
	#draw the button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
	#making the most recently drawn screen visible
	pygame.display.flip()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#check for any bullets that have hit alien and get rid of the hit once
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
		  stats.score+=ai_settings.alien_points*len(aliens)
		  sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#if the entire fleet is destroyed start a new level
		bullets.empty()
		ai_settings.increase_speed()
		#increase level
		stats.level+=1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#update bullet position and get rid of old bullets
	bullets.update()
	#get rid of disappeared bullets
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	#check the terminal for the count of the existing bullets and remove the print
	#print(len(bullets))
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#respond to ship hit by alien
	if stats.ships_left > 0:
	  stats.ships_left -= 1
	  sb.prep_ships()
	  aliens.empty()
	  bullets.empty()
	  create_fleet(ai_settings, screen, ship, aliens)
	  ship.center_ship()
	  #pause
	  sleep(0.5)
	else:
		stats.game_active = False
		#make the cursor visible
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#check if any aliens have reached the bottom of the screen
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			#threet this the same as if the ship got hit
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#check if the fleet is at an edge and update the position of all aliens
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	#look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

	#look for aliens hitting the bottom
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)