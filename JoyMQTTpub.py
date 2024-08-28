import pygame
import sys
import json
from paho.mqtt import client as mqtt

class inputWindow():
    def __init__(self, width, height, title, fontSize):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, fontSize)
        self.title = title
        pygame.display.set_caption(self.title)
    
    def clear(self):
        self.screen.fill((0, 0, 0))
    
    def update(self):
        pygame.display.flip()
    
    def draw_text(self, text, position, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

        


def joyMQTTLoop(visualize:bool):

    # Load configuration from a JSON file
    with open('config.json') as f:
        config = json.load(f)

    deadzone = config['deadzone']
    broker_host = config['broker_host']
    broker_port = config['broker_port']
    topic = config['topic_vel']



    client = mqtt.Client()
    client.connect(broker_host, broker_port)

    # Initialize Pygame
    pygame.init()

    # Set up the display
    #screen = pygame.display.set_mode((300, 160))
    if visualize:
        Screen = inputWindow(300, 160, 'Joystick Input Display', 36)

    # Initialize the joystick
    pygame.joystick.init()

    # Check for joystick
    if pygame.joystick.get_count() == 0:
        print("No joystick connected.")
        sys.exit()

    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Main loop to read joystick input
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Display joystick information
        #draw_text(screen, f"Joystick name: {joystick.get_name()}", (20, 20))
        #draw_text(screen, f"Number of axes: {joystick.get_numaxes()}", (20, 60))
        #draw_text(screen, f"Number of buttons: {joystick.get_numbuttons()}", (20, 100))
        deadman_trigger = joystick.get_button(4)
        
        if deadman_trigger:
            speed_normal = joystick.get_axis(0) if abs(joystick.get_axis(0)) >= deadzone else 0
            speed_linear = -joystick.get_axis(1) if abs(joystick.get_axis(1)) >= deadzone else 0
            speed_angular = joystick.get_axis(2) if abs(joystick.get_axis(2)) >= deadzone else 0
        else:
            speed_normal = 0
            speed_linear = 0
            speed_angular = 0



        speed_json = json.dumps({
        "v": speed_linear,
        "vn": speed_normal,
        "w": speed_angular
        })

        #draw_text(screen, f"Speed JSON: {speed_json}", (20, 300))
        client.publish(topic, speed_json)

        if visualize:
        # Clear the screen
            Screen.clear()
            Screen.draw_text(f"Linear speed: {speed_linear:.2f}", (20, 10))
            Screen.draw_text(f"Normal speed: {speed_normal:.2f}", (20, 50))
            Screen.draw_text(f"Angular speed: {speed_angular:.2f}", (20, 90))
            Screen.draw_text(f"Deadman trigger: {deadman_trigger}", (20, 130))
            Screen.update()

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    joyMQTTLoop(True)
