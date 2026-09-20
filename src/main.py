import pygame
from pygame.locals import K_ESCAPE, K_LEFT, K_RIGHT, KEYDOWN, QUIT

# ---------------------------
# Configuración general
# ---------------------------
WIDTH, HEIGHT = 480, 700
FPS = 60

# Colores utilizados en el juego
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
DARK_GRAY = (35, 35, 35)
ROAD_EDGE = (120, 120, 120)
PLAYER_COLOR = (30, 144, 255)

# Dimensiones de la carretera y del auto del jugador
ROAD_WIDTH = 260
LANE_COUNT = 3
PLAYER_WIDTH = 52
PLAYER_HEIGHT = 92
PLAYER_SPEED = 7

# ---------------------------
# Clase del vehículo del jugador
# ---------------------------
class PlayerCar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def update(self, keys):
        """Mueve el auto según las teclas pulsadas."""
        if keys[K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Limita el movimiento para que el auto no salga de la carretera
        road_left = (WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        max_left = road_left
        max_right = road_right - PLAYER_WIDTH

        self.rect.x = max(max_left, min(self.rect.x, max_right))

    def draw(self, screen):
        """Dibuja el auto del jugador en la pantalla."""
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

        # Ventana delantera
        pygame.draw.rect(screen, (20, 90, 180), (self.rect.x + 12, self.rect.y + 10, 28, 18))

        # Luces traseros
        pygame.draw.rect(screen, (255, 90, 90), (self.rect.x + 10, self.rect.y + self.rect.height - 12, 10, 10))
        pygame.draw.rect(screen, (255, 90, 90), (self.rect.x + self.rect.width - 20, self.rect.y + self.rect.height - 12, 10, 10))

# ---------------------------
# Funciones de dibujo
# ---------------------------

def draw_background(screen):
    """Pinta el fondo general del juego."""
    screen.fill(BLACK)

    # Bordes exteriores de la carretera
    road_left = (WIDTH - ROAD_WIDTH) // 2
    road_right = road_left + ROAD_WIDTH

    # Lado izquierdo y derecho de la carretera
    pygame.draw.rect(screen, ROAD_EDGE, (road_left - 25, 0, 25, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE, (road_right, 0, 25, HEIGHT))

    # Carretera principal
    pygame.draw.rect(screen, GRAY, (road_left, 0, ROAD_WIDTH, HEIGHT))

    # Carriles
    lane_width = ROAD_WIDTH / LANE_COUNT
    for i in range(1, LANE_COUNT):
        lane_x = road_left + i * lane_width
        pygame.draw.line(screen, WHITE, (lane_x, 0), (lane_x, HEIGHT), 3)

    # Rayas de marca de carril para dar sensación de movimiento
    stripe_height = 30
    stripe_width = 10
    for y in range(-50, HEIGHT + 50, 60):
        for i in range(LANE_COUNT - 1):
            lane_x = road_left + (i + 1) * lane_width
            pygame.draw.rect(
                screen,
                WHITE,
                (lane_x - stripe_width // 2, y, stripe_width, stripe_height),
            )


def draw_player(screen, player):
    """Dibuja el vehículo del jugador."""
    player.draw(screen)


# ---------------------------
# Función principal del juego
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Escape")
    clock = pygame.time.Clock()

    # Posición inicial del auto del jugador
    road_left = (WIDTH - ROAD_WIDTH) // 2
    player_x = road_left + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2)
    player = PlayerCar(player_x, HEIGHT - 150)

    running = True

    while running:
        # Control del tiempo del juego
        clock.tick(FPS)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # Teclas presionadas por el jugador
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Dibujo del juego
        draw_background(screen)
        draw_player(screen, player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
