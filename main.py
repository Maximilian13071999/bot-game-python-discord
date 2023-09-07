import random
import asyncio
import discord
import pygame
from discord.ext import commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)

settings = {
    'token': 'MTAyNTQzNDc3Mjc2MTIyMzM1MQ.Gmdt6f.2sx4qfQkdpZESQmJph5Lt_pxnWu0muRUGLtZSQ',
    'bot': 'Goosebot3',
    'id': 1025434772761223351,
    'prefix': '!'
}

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

size = (750, 750)
pygame.init()
screen = pygame.display.set_mode(size)

background = pygame.image.load("wood.jpg")
background = pygame.transform.scale(background, (750, 750))

win = pygame.image.load("win.png")
win = pygame.transform.scale(win, (750, 750))

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("circle.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brickwall.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y

class Person(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("NAME.jpg")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y

person = Person(20, 20)
circle1 = Circle(250, 50)
wall1 = Obstacle(0, 300, 200, 200)

circles = 0
is_win = False

old_message = None

async def update_screen(message, is_start=False):
    global circles, is_win, old_message
    if is_win == True:
        return
    screen.blit(background, (0, 0))
    screen.blit(person.image, person.rect)
    if person.rect.colliderect(circle1.rect):
        circle1.rect.x = random.randint(100, 650)
        circle1.rect.y = random.randint(100, 650)
        circles += 1
        if circles >= 1:
            screen.blit(win, (0, 0))
            is_win = True

    if not is_win:
        screen.blit(circle1.image, circle1.rect)
        screen.blit(wall1.image, wall1.rect)
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f'Circles: {circles}', False, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    pygame.image.save(screen, "screenshot.jpeg")
    if (is_start == True):
        old_message = await message.channel.send(file=discord.File("screenshot.jpeg"))
    else:
        await message.delete()
        await old_message.delete()
        old_message = await message.channel.send(file=discord.File("screenshot.jpeg"))

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'start':
        await update_screen(message, is_start=True)
    if message.content == "left":
        person.rect.x -= 25
        await update_screen(message)
    if message.content == "right":
        person.rect.x += 25
        await update_screen(message)
    if message.content == 'up':
        person.rect.y -= 25
        await update_screen(message)
    if message.content == 'down':
        person.rect.y += 25
        if not person.rect.colliderect(wall1.rect):
            await update_screen(message)
        else:
            person.rect.y -= 25
            await update_screen(message)

bot.run(settings['token'])