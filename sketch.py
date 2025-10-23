# https://managing.blue/2025/10/23/a-bare-whiteboard-application/

import pygame
import sys
import argparse


options = argparse.ArgumentParser(description='Start a pygame window with configurable dimensions')
options.add_argument('--width', type=int, default=800, help='Window width (default: 800)')
options.add_argument('--height', type=int, default=600, help='Window height (default: 600)')
args = options.parse_args()

pygame.init()

screen = pygame.display.set_mode((args.width, args.height))
pygame.display.set_caption('pygame sketch')
clock = pygame.time.Clock()
a = (-1, -1)

screen.fill((250, 250, 160))
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONUP:
			a = (-1, -1)

	mouse_buttons = pygame.mouse.get_pressed()
	if mouse_buttons[0]:
		if a[0] == -1:
			a = pygame.mouse.get_pos()
		else:
			b = pygame.mouse.get_pos()
			pygame.draw.line(screen, 'red', a, b, 2)
			a = b

	pygame.display.flip()
	clock.tick(60)