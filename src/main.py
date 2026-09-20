import random
import pygame
from pygame.locals import K_ESCAPE, K_LEFT, K_RIGHT, K_r, K_RETURN, KEYDOWN, QUIT

# ---------------------------
# Configuración general
# ---------------------------
WIDTH, HEIGHT = 480, 700
FPS = 60

# Colores principales del juego
WHITE = (255, 255, 255)
BLACK = (10, 10, 18)
GRAY = (54, 57, 64)
DARK_GRAY = (27, 30, 35)
ROAD_EDGE = (120, 120, 120)
ROAD_SURFACE = (65, 68, 73)
LANE_LINE = (255, 255, 255)
PLAYER_COLOR = (32, 144, 255)
ENEMY_COLORS = [(220, 90, 90), (255, 165, 0), (95, 158, 80), (179, 81, 255)]
HUD_BG = (18, 20, 25)
TEXT_COLOR = (245, 245, 245)
ACCENT = (255, 210, 60)

# Dimensiones del juego y vehículos
ROAD_WIDTH = 260
LANE_COUNT = 3
PLAYER_WIDTH = 52
PLAYER_HEIGHT = 92
ENEMY_WIDTH = 52
ENEMY_HEIGHT = 92
PLAYER_SPEED = 7
SCROLL_SPEED = 2
MAX_ACTIVE_ENEMIES = 2

# ---------------------------
# Clase del vehículo del jugador
# ---------------------------
class PlayerCar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def update(self, keys):
        """Mueve el auto según las teclas presionadas."""
        if keys[K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        road_left = (WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        self.rect.x = max(road_left, min(self.rect.x, road_right - PLAYER_WIDTH))

    def draw(self, screen):
        """Dibuja el auto del jugador con un aspecto más detallado."""
        draw_vehicle(screen, self.rect, PLAYER_COLOR, is_player=True)


# ---------------------------
# Clase del vehículo enemigo
# ---------------------------
class EnemyCar:
    def __init__(self, lane, y, color):
        self.lane = lane
        self.speed = random.uniform(4.2, 6.4)
        self.color = color
        lane_width = ROAD_WIDTH / LANE_COUNT
        road_left = (WIDTH - ROAD_WIDTH) // 2
        x = road_left + (lane * lane_width) + (lane_width / 2) - (ENEMY_WIDTH / 2)
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def update(self):
        """Desplaza el enemigo hacia abajo con velocidad variable."""
        self.rect.y += self.speed

    def draw(self, screen):
        """Dibuja el enemigo con colores y detalles distintos."""
        draw_vehicle(screen, self.rect, self.color, is_player=False)


# ---------------------------
# Funciones de dibujo
# ---------------------------
def draw_vehicle(screen, rect, color, is_player):
    """Dibuja un vehículo genérico con techo, ventanas y focos."""
    x, y, width, height = rect

    # Sombra para dar profundidad
    shadow = pygame.Rect(x + 5, y + 6, width, height)
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=12)

    # Cuerpo principal
    pygame.draw.rect(screen, color, rect, border_radius=12)

    # Carrocería más oscura para resaltar contornos
    body_dark = pygame.Rect(x + 8, y + 10, width - 16, height - 20)
    pygame.draw.rect(screen, tuple(max(0, c - 25) for c in color), body_dark, border_radius=10)

    # Ventanas
    window_color = (190, 220, 255) if is_player else (230, 230, 230)
    pygame.draw.rect(screen, window_color, (x + 10, y + 14, width - 20, 22), border_radius=6)
    pygame.draw.rect(screen, window_color, (x + 14, y + 38, width - 28, 18), border_radius=5)

    # Focos
    if is_player:
        headlight_color = (255, 255, 180)
        tail_light_color = (255, 90, 90)
    else:
        headlight_color = (255, 210, 120)
        tail_light_color = (255, 80, 80)

    pygame.draw.rect(screen, headlight_color, (x + 10, y + 8, 10, 8), border_radius=3)
    pygame.draw.rect(screen, headlight_color, (x + width - 20, y + 8, 10, 8), border_radius=3)
    pygame.draw.rect(screen, tail_light_color, (x + 10, y + height - 18, 10, 8), border_radius=3)
    pygame.draw.rect(screen, tail_light_color, (x + width - 20, y + height - 18, 10, 8), border_radius=3)

    # Ruedas
    wheel_color = (20, 20, 20)
    wheel_offset = 12
    wheel_size = 9
    pygame.draw.rect(screen, wheel_color, (x + 8, y + 10, wheel_size, wheel_size), border_radius=2)
    pygame.draw.rect(screen, wheel_color, (x + width - 18, y + 10, wheel_size, wheel_size), border_radius=2)
    pygame.draw.rect(screen, wheel_color, (x + 8, y + height - 20, wheel_size, wheel_size), border_radius=2)
    pygame.draw.rect(screen, wheel_color, (x + width - 18, y + height - 20, wheel_size, wheel_size), border_radius=2)


def draw_background(screen, road_scroll_y):
    """Pinta un fondo de carretera con detalles simples pero más vistosos."""
    screen.fill(BLACK)

    # Paisaje lejano: montañas y árboles estilizados
    mountain_color = (30, 40, 55)
    for i in range(0, WIDTH + 80, 90):
        pts = [(i, 220), (i + 40, 130), (i + 80, 220)]
        pygame.draw.polygon(screen, mountain_color, pts)

    # Línea superior de la carretera para dar profundidad
    road_left = (WIDTH - ROAD_WIDTH) // 2
    road_right = road_left + ROAD_WIDTH

    # Laterales de la carretera
    pygame.draw.rect(screen, ROAD_EDGE, (road_left - 28, 0, 28, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE, (road_right, 0, 28, HEIGHT))

    # Base de la carretera
    pygame.draw.rect(screen, ROAD_SURFACE, (road_left, 0, ROAD_WIDTH, HEIGHT))

    # Borde pintado de la carretera
    pygame.draw.rect(screen, ACCENT, (road_left - 2, 0, 2, HEIGHT))
    pygame.draw.rect(screen, ACCENT, (road_right, 0, 2, HEIGHT))

    # Carriles visibles
    lane_width = ROAD_WIDTH / LANE_COUNT
    for i in range(1, LANE_COUNT):
        lane_x = road_left + i * lane_width
        pygame.draw.line(screen, LANE_LINE, (lane_x, 0), (lane_x, HEIGHT), 3)

    # Líneas de referencia para simular movimiento
    stripe_height = 34
    stripe_width = 10
    for y in range(-60, HEIGHT + 60, 60):
        draw_y = (y + road_scroll_y) % (HEIGHT + 60)
        for i in range(LANE_COUNT - 1):
            lane_x = road_left + (i + 1) * lane_width
            pygame.draw.rect(screen, LANE_LINE, (lane_x - stripe_width // 2, draw_y, stripe_width, stripe_height), border_radius=3)

    # Detalles laterales: postes o faroles pequeños
    for offset in range(0, HEIGHT + 50, 90):
        y = (offset + road_scroll_y * 2) % (HEIGHT + 90)
        pygame.draw.rect(screen, (180, 180, 180), (road_left - 18, y, 6, 22), border_radius=2)
        pygame.draw.rect(screen, (180, 180, 180), (road_right + 12, y, 6, 22), border_radius=2)

    # Pequeñas marcas de borde para mejorar la estética
    for y in range(0, HEIGHT + 40, 80):
        pygame.draw.rect(screen, (200, 200, 200), (road_left - 10, y, 6, 26), border_radius=3)
        pygame.draw.rect(screen, (200, 200, 200), (road_right + 4, y, 6, 26), border_radius=3)


def draw_hud(screen, is_game_over):
    """Muestra una pequeña interfaz informativa sin complicar la pantalla."""
    panel = pygame.Rect(0, 0, WIDTH, 46)
    pygame.draw.rect(screen, HUD_BG, panel)

    title_font = pygame.font.SysFont("arial", 18, bold=True)
    info_font = pygame.font.SysFont("arial", 12)

    title = title_font.render("ROAD ESCAPE", True, TEXT_COLOR)
    status = "RUNNING" if not is_game_over else "GAME OVER"
    status_text = info_font.render(status, True, ACCENT if not is_game_over else (255, 90, 90))

    screen.blit(title, (18, 12))
    screen.blit(status_text, (WIDTH - 120, 16))


def draw_game_over(screen):
    """Muestra la pantalla de fin de partida con mensaje y opción de reinicio."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("arial", 42, bold=True)
    font_small = pygame.font.SysFont("arial", 20)

    title = font_big.render("GAME OVER", True, (255, 100, 100))
    restart = font_small.render("Presiona R para reiniciar", True, WHITE)
    quit_msg = font_small.render("ESC para salir", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, HEIGHT // 2 + 45))


# ---------------------------
# Generación de enemigos
# ---------------------------
def spawn_enemy(enemies):
    """Genera un enemigo en un carril aleatorio y evita que aparezcan demasiado juntos."""
    if len(enemies) >= MAX_ACTIVE_ENEMIES:
        return False

    lane_order = list(range(LANE_COUNT))
    random.shuffle(lane_order)

    for lane in lane_order:
        # Se comprueba que el carril no esté demasiado cargado cerca de la parte superior
        too_close = False
        for enemy in enemies:
            if enemy.lane == lane and enemy.rect.top < 170:
                too_close = True
                break
            if abs(enemy.lane - lane) == 1 and enemy.rect.top < 110:
                too_close = True
                break

        if too_close:
            continue

        y = -ENEMY_HEIGHT - random.randint(60, 180)
        enemies.append(EnemyCar(lane, y, random.choice(ENEMY_COLORS)))
        return True

    return False


# ---------------------------
# Reinicio del juego
# ---------------------------
def reset_game():
    """Devuelve el estado del juego al inicio para reiniciar la partida."""
    road_left = (WIDTH - ROAD_WIDTH) // 2
    player_x = road_left + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2)
    player = PlayerCar(player_x, HEIGHT - 150)
    enemies = []
    road_scroll_y = 0
    spawn_timer = 0.0
    next_spawn_delay = random.uniform(1.0, 2.2)
    is_game_over = False
    return player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, is_game_over


# ---------------------------
# Función principal del juego
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Escape")
    clock = pygame.time.Clock()

    player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, is_game_over = reset_game()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        # Manejo de eventos tanto en juego como en pantalla final
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if is_game_over and event.key in (K_r, K_RETURN):
                    player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, is_game_over = reset_game()

        if not is_game_over:
            # Movimiento visual de la carretera
            road_scroll_y = (road_scroll_y + SCROLL_SPEED) % 120

            # Movimiento del jugador siguiendo la misma mecánica que antes
            keys = pygame.key.get_pressed()
            player.update(keys)

            # Generación aleatoria de enemigos con tiempo de espera variable
            spawn_timer += dt
            if spawn_timer >= next_spawn_delay:
                if spawn_enemy(enemies):
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(1.0, 2.3)
                else:
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(0.6, 1.3)

            # Actualización de enemigos y eliminación cuando salen de la pantalla
            for enemy in enemies[:]:
                enemy.update()
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(0.8, 1.9)

                if player.rect.colliderect(enemy.rect):
                    is_game_over = True
                    break

        # Dibujo del juego
        draw_background(screen, road_scroll_y)
        draw_hud(screen, is_game_over)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        if is_game_over:
            draw_game_over(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
