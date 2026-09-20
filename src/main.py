import random
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
ROAD_EDGE = (120, 120, 120)
PLAYER_COLOR = (30, 144, 255)
ENEMY_COLOR = (220, 70, 70)

# Dimensiones de la carretera y los vehículos
ROAD_WIDTH = 260
LANE_COUNT = 3
PLAYER_WIDTH = 52
PLAYER_HEIGHT = 92
ENEMY_WIDTH = 52
ENEMY_HEIGHT = 92
PLAYER_SPEED = 7
SCROLL_SPEED = 2
ENEMY_SPEED = 4
MAX_ENEMIES = 4

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
# Clase del vehículo enemigo
# ---------------------------
class EnemyCar:
    def __init__(self, lane, y):
        self.lane = lane
        lane_width = ROAD_WIDTH / LANE_COUNT
        road_left = (WIDTH - ROAD_WIDTH) // 2
        x = road_left + (lane * lane_width) + (lane_width / 2) - (ENEMY_WIDTH / 2)
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def update(self):
        """Desplaza el enemigo hacia abajo."""
        self.rect.y += ENEMY_SPEED

    def draw(self, screen):
        """Dibuja el auto enemigo en la pantalla."""
        pygame.draw.rect(screen, ENEMY_COLOR, self.rect)

        # Ventana delantera
        pygame.draw.rect(screen, (180, 20, 20), (self.rect.x + 12, self.rect.y + 10, 28, 18))

        # Luces traseros
        pygame.draw.rect(screen, (255, 210, 90), (self.rect.x + 10, self.rect.y + self.rect.height - 12, 10, 10))
        pygame.draw.rect(screen, (255, 210, 90), (self.rect.x + self.rect.width - 20, self.rect.y + self.rect.height - 12, 10, 10))


# ---------------------------
# Funciones de apoyo
# ---------------------------
def spawn_enemy(enemies):
    """Crea un vehículo enemigo en un carril aleatorio y evita que aparezcan demasiado juntos."""
    if len(enemies) >= MAX_ENEMIES:
        return False

    # Se revisan los carriles en orden aleatorio para variar los spawns
    lane_order = list(range(LANE_COUNT))
    random.shuffle(lane_order)

    for lane in lane_order:
        # La posición inicial se genera arriba de la pantalla
        y = -ENEMY_HEIGHT - random.randint(30, 170)

        # Se evita que dos enemigos del mismo carril aparezcan demasiado cerca entre sí
        can_spawn = True
        for enemy in enemies:
            if enemy.lane == lane and abs(enemy.rect.y - y) < 120:
                can_spawn = False
                break

        if can_spawn:
            enemies.append(EnemyCar(lane, y))
            return True

    return False


def draw_background(screen, road_scroll_y):
    """Pinta el fondo del juego y el movimiento de la carretera."""
    screen.fill(BLACK)

    road_left = (WIDTH - ROAD_WIDTH) // 2
    road_right = road_left + ROAD_WIDTH

    # Bordes exteriores de la carretera
    pygame.draw.rect(screen, ROAD_EDGE, (road_left - 25, 0, 25, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE, (road_right, 0, 25, HEIGHT))

    # Carretera principal
    pygame.draw.rect(screen, GRAY, (road_left, 0, ROAD_WIDTH, HEIGHT))

    # Carriles
    lane_width = ROAD_WIDTH / LANE_COUNT
    for i in range(1, LANE_COUNT):
        lane_x = road_left + i * lane_width
        pygame.draw.line(screen, WHITE, (lane_x, 0), (lane_x, HEIGHT), 3)

    # Rayas que simulan el movimiento de la carretera
    stripe_height = 30
    stripe_width = 10
    stripe_spacing = 60
    for y in range(-stripe_spacing, HEIGHT + stripe_spacing, stripe_spacing):
        draw_y = (y + road_scroll_y) % (HEIGHT + stripe_spacing)
        for i in range(LANE_COUNT - 1):
            lane_x = road_left + (i + 1) * lane_width
            pygame.draw.rect(
                screen,
                WHITE,
                (lane_x - stripe_width // 2, draw_y, stripe_width, stripe_height),
            )


# ---------------------------
# Función principal del juego
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Escape")
    clock = pygame.time.Clock()

    road_left = (WIDTH - ROAD_WIDTH) // 2
    player_x = road_left + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2)
    player = PlayerCar(player_x, HEIGHT - 150)

    # Enemigos iniciales en pantalla
    enemies = []
    for _ in range(3):
        spawn_enemy(enemies)

    road_scroll_y = 0
    running = True

    while running:
        # Control del tiempo del juego
        clock.tick(FPS)

        # Movimiento visual de la carretera ligeramente más lento que los enemigos
        road_scroll_y = (road_scroll_y + SCROLL_SPEED) % 60

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Actualización y limpieza de enemigos
        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                spawn_enemy(enemies)

        # Dibujo del juego
        draw_background(screen, road_scroll_y)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
