
import sys, pygame 
# Slow down speed of game
clock = pygame.time.Clock()
fps = 90

#initialsie the font
pygame.font.init()

# score countet

font_name = pygame.font.match_font("comicsansms.ttf", 20)


class Game:
    def __init__(self):
        #Width and height of screen
        self.width = 800
        self.height = 600


        #Creating screen
        self.screen = pygame.display.set_mode((self.width,self.height))
        #Setting name of window
        pygame.display.set_caption("Space Invaders")
        
        #Loading background
        self.bg = pygame.image.load("background.jpg")
        #Set background to size of screen
        self.bg = pygame.transform.scale(self.bg,(800,600))


    def draw_bg(self):
        #draw background onto screen
        self.screen.blit(self.bg,(0,0))

    # Display message to the screen     
    def score_counter(self,message,colour,font_size,x,y):
        self.font = pygame.font.SysFont(font_name,font_size)
        self.text = self.font.render(message,True,colour)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (x,y)
        self.screen.blit(self.text, self.text_rect)



    def main_loop(self):
        run = True
        while run:
            #Slowing down the movement of all the objects in the game, without this the aliens would move to quick accross the screen
            clock.tick(fps) 
            #calling the draw background function
            self.draw_bg()
            for event in pygame.event.get():
                #Close pygame window if event.type == pygame.QUIT
                if event.type == pygame.QUIT:
                    run = False

            #update spaceship
            spaceship.update()

            #update sprite group
            bullet_group.update()
            alien_group.update()  

            #draw sprite group
            spaceship_group.draw(self.screen)   
            bullet_group.draw(self.screen)   
            alien_group.draw(self.screen)

            #printing score counter to screen
            self.score_counter("Score: " + str(spaceship.score), (255,255,255), 40 , 60, 30)

            # update scrren
            pygame.display.update()



#Create SpaceShip class as child class of pygame Sprite Class
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,x,y):
        #Inheriting the functionality from the pygame class Sprite for my spaceship class
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("baseshipa.ico")
        # create rectangle from the Spaceship image
        self.rect = self.image.get_rect() 
        self.rect.center = [x,y]
        self.score = 0


        # when the bullet was created
        self.last_shot = pygame.time.get_ticks() 
        


    def update(self):
        #set movement speed
        speed = 3

        #set a cooldown variable for speed of bullets
        cooldown = 1000


        #moves spaceship accross while holding down keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += speed

        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            #create a bullet instance
            bullet = Bullets(self.rect.centerx, self.rect.top)
            #adding the bullets to the sprite group
            bullet_group.add(bullet)
            # reset the timer 
            self.last_shot = time_now

        #if the alien collides with the spaceship we want to destroy the spaceship
        if pygame.sprite.spritecollide(self,alien_group, True):
            self.kill()
            #comes out of the pygame window when the spaceship dies
            pygame.quit()
            


#Create SpaceShip class as child class of pygame Sprite Class
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #load in image
        self.image = pygame.image.load("bullet.png")
        #transform it to the size I want
        self.image = pygame.transform.scale(self.image,(20,20))
        # create rectangle from the bullet image
        self.rect = self.image.get_rect()
        # set centre point of the rectangle to x and y
        self.rect.center = [x,y]






    def update(self):
        #bullet moves up the screen at speed of 5
        self.rect.y -= 5
        if self.rect.bottom < 0:
            #kills instance of bullet that has gone off the screen
            self.kill() 
        #kills the alien if it collides with the bullet
        if pygame.sprite.spritecollide(self,alien_group, True):
            self.kill()
            spaceship.score += 5
            
        
    
class Aliens(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #loading in image for aliens
        self.image = pygame.image.load("alien.png")
        self.image = pygame.transform.scale(self.image,(40,40))
        # create rectangle from alien image
        self.rect = self.image.get_rect() 
        self.rect.center = [x,y]
        #check to see how far aliens are accross the screen
        self.move_counter = 0 
        #start aliens moving to the right
        self.move_direction = 1 

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
         #checks for when number is minus and plus
        if abs(self.move_counter) > 125: 
            # once it reaches a vlaue of 125 the aliens will begin going in the other direction
            self.move_direction *= -1  
            # moves aliens down each time it hits the border and goes in the opposite direction
            self.rect.y = self.rect.y  + 10
            self.move_counter *= self.move_direction
        
        

    

    
    

#sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group() # empty group for all my aliens to be stored

#cretaing the grid of aliens with the alien class
# iternates through the grid and create all the instances and add them to the group 
def create_aliens(): 
    #rows and columns of aliens that i want
    rows = 5
    cols = 11
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(150  + item * 50, 100 + row * 45)
            #adds the 55 aliens to the sprite group
            alien_group.add(alien) 
            # trying to get 55 aliens to be created again when all the aliens die 



#call the function to create the aliens
create_aliens()

#create instance of player 
spaceship = SpaceShip(int(800 /2), 650 - 100)
spaceship_group.add(spaceship)

#how to run the game
if __name__ == "__main__":
    mygame = Game()
    mygame.main_loop()


        
