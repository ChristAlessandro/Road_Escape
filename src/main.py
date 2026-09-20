import os
import random
import pygame
from pygame.locals import K_ESCAPE, K_LEFT, K_RIGHT, K_r, K_RETURN, KEYDOWN, QUIT

# ---------------------------
# Configuración general
# ---------------------------
WIDTH, HEIGHT = 480, 700
FPS = 60
HIGH_SCORE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "highscore.txt"))

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
BASE_SCORE_RATE = 25
MAX_DIFFICULTY_LEVEL = 8

# ---------------------------
# Sistemas de puntuación y récord
# ---------------------------
def load_high_score():
    """Carga el récord guardado en un archivo local del proyecto."""
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            score = int(file.read().strip())
            return max(0, score)
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    """Guarda el récord en disco para mantenerlo entre partidas."""
    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
        file.write(str(max(0, int(score))))


def get_difficulty_level(score):
    """Calcula el nivel de dificultad en función de la puntuación acumulada."""
    return min(MAX_DIFFICULTY_LEVEL, 1 + score // 350)


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
    def __init__(self, lane, y, color, speed=None):
        self.lane = lane
        self.speed = speed if speed is not None else random.uniform(4.2, 6.4)
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
    """Dibuja un auto con forma más reconocible, manteniendo el tamaño y hitbox actuales."""
    x, y, width, height = rect

    # Sombra para dar sensación de profundidad
    shadow = pygame.Rect(x + 4, y + 6, width, height)
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=14)

    # Carrocería principal
    body = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, body, border_radius=14)

    # Zona de motor y maletero para dar forma de auto
    pygame.draw.rect(screen, tuple(max(0, c - 18) for c in color), (x + 7, y + 12, width - 14, height - 26), border_radius=12)

    # Techo y parabrisas
    window_color = (198, 220, 255) if is_player else (220, 224, 230)
    roof = pygame.Rect(x + 10, y + 14, width - 20, 22)
    pygame.draw.rect(screen, window_color, roof, border_radius=6)
    pygame.draw.rect(screen, window_color, (x + 12, y + 38, width - 24, 16), border_radius=5)

    # Parachoques
    front_bumper = pygame.Rect(x + width - 6, y + 18, 6, height - 36)
    rear_bumper = pygame.Rect(x, y + 18, 6, height - 36)
    pygame.draw.rect(screen, (80, 80, 80), front_bumper, border_radius=3)
    pygame.draw.rect(screen, (80, 80, 80), rear_bumper, border_radius=3)

    # Faros delanteros y traseros
    if is_player:
        headlight_color = (255, 248, 170)
        taillight_color = (255, 90, 90)
    else:
        headlight_color = (255, 220, 120)
        taillight_color = (255, 80, 80)

    pygame.draw.rect(screen, headlight_color, (x + 10, y + 8, 10, 8), border_radius=3)
    pygame.draw.rect(screen, headlight_color, (x + width - 20, y + 8, 10, 8), border_radius=3)
    pygame.draw.rect(screen, taillight_color, (x + 10, y + height - 18, 10, 8), border_radius=3)
    pygame.draw.rect(screen, taillight_color, (x + width - 20, y + height - 18, 10, 8), border_radius=3)

    # Llantas más grandes y visibles
    wheel_color = (20, 20, 20)
    wheel_size = 9
    wheel_positions = [
        (x + 8, y + 10),
        (x + width - 18, y + 10),
        (x + 8, y + height - 20),
        (x + width - 18, y + height - 20),
    ]
    for wx, wy in wheel_positions:
        pygame.draw.rect(screen, wheel_color, (wx, wy, wheel_size, wheel_size), border_radius=2)

    # Línea superior para diferenciar el jugador del resto
    if is_player:
        pygame.draw.rect(screen, (255, 255, 255), (x + 14, y + 16, width - 28, 3), border_radius=2)


def draw_background(screen, road_scroll_y):
    """Pinta un entorno de carretera con bordes, carriles y detalles laterales."""
    screen.fill(BLACK)

    # Fondo basado en montañas para dar sensación de paisaje
    mountain_color = (28, 36, 50)
    for i in range(-20, WIDTH + 80, 90):
        pts = [(i, 220), (i + 30, 140), (i + 60, 220)]
        pygame.draw.polygon(screen, mountain_color, pts)

    # Barreras laterales y carretera principal
    road_left = (WIDTH - ROAD_WIDTH) // 2
    road_right = road_left + ROAD_WIDTH

    pygame.draw.rect(screen, ROAD_EDGE, (road_left - 28, 0, 28, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE, (road_right, 0, 28, HEIGHT))
    pygame.draw.rect(screen, ROAD_SURFACE, (road_left, 0, ROAD_WIDTH, HEIGHT))

    # Bordes de la carretera para separarla del entorno
    pygame.draw.rect(screen, ACCENT, (road_left - 2, 0, 2, HEIGHT))
    pygame.draw.rect(screen, ACCENT, (road_right, 0, 2, HEIGHT))

    # Línea divisoria de carriles más visibles
    lane_width = ROAD_WIDTH / LANE_COUNT
    for i in range(1, LANE_COUNT):
        lane_x = road_left + i * lane_width
        pygame.draw.line(screen, LANE_LINE, (lane_x, 0), (lane_x, HEIGHT), 3)

    # Líneas de movimiento con efecto visual de desplazamiento
    stripe_height = 34
    stripe_width = 10
    for y in range(-60, HEIGHT + 60, 60):
        draw_y = (y + road_scroll_y) % (HEIGHT + 60)
        for i in range(LANE_COUNT - 1):
            lane_x = road_left + (i + 1) * lane_width
            pygame.draw.rect(screen, LANE_LINE, (lane_x - stripe_width // 2, draw_y, stripe_width, stripe_height), border_radius=3)

    # Elementos del entorno a los lados de la carretera
    side_color = (70, 90, 75)
    for offset in range(0, HEIGHT + 60, 90):
        y = (offset + road_scroll_y * 2) % (HEIGHT + 90)
        tree_x_left = road_left - 28
        tree_x_right = road_right + 18

        pygame.draw.rect(screen, (135, 135, 135), (tree_x_left, y + 8, 5, 22), border_radius=2)
        pygame.draw.rect(screen, side_color, (tree_x_left - 12, y, 18, 18), border_radius=9)
        pygame.draw.rect(screen, (120, 120, 120), (tree_x_right, y + 8, 5, 22), border_radius=2)
        pygame.draw.rect(screen, side_color, (tree_x_right - 6, y, 18, 18), border_radius=9)

    # Señales simples para dar más profundidad visual
    for y in range(0, HEIGHT + 40, 80):
        pygame.draw.rect(screen, (200, 200, 200), (road_left - 10, y, 6, 26), border_radius=3)
        pygame.draw.rect(screen, (200, 200, 200), (road_right + 4, y, 6, 26), border_radius=3)


def draw_hud(screen, score, high_score, difficulty_level, is_game_over):
    """Muestra la información principal sin cubrir la carretera."""
    panel = pygame.Rect(0, 0, WIDTH, 60)
    pygame.draw.rect(screen, HUD_BG, panel)

    title_font = pygame.font.SysFont("arial", 18, bold=True)
    info_font = pygame.font.SysFont("arial", 11)

    title = title_font.render("ROAD ESCAPE", True, TEXT_COLOR)
    score_text = info_font.render(f"Score: {int(score)}", True, ACCENT)
    record_text = info_font.render(f"Record: {int(high_score)}", True, WHITE)
    level_text = info_font.render(f"Nivel: {difficulty_level}", True, (120, 220, 255))
    status = "RUNNING" if not is_game_over else "GAME OVER"
    status_text = info_font.render(status, True, ACCENT if not is_game_over else (255, 90, 90))

    screen.blit(title, (18, 12))
    screen.blit(score_text, (18, 34))
    screen.blit(record_text, (130, 34))
    screen.blit(level_text, (235, 34))
    screen.blit(status_text, (WIDTH - 100, 18))


def draw_game_over(screen, score, high_score):
    """Muestra la pantalla de fin de partida con la puntuación y el récord."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    header = pygame.Rect(70, 210, WIDTH - 140, 210)
    pygame.draw.rect(screen, (30, 30, 35), header, border_radius=18)
    pygame.draw.rect(screen, (255, 90, 90), header, 2, border_radius=18)

    font_big = pygame.font.SysFont("arial", 42, bold=True)
    font_small = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)

    title = font_big.render("GAME OVER", True, (255, 110, 110))
    score_text = font_small.render(f"Puntuación: {int(score)}", True, WHITE)
    record_text = font_small.render(f"Récord: {int(high_score)}", True, ACCENT)
    restart = font_small.render("Presiona R para reiniciar", True, WHITE)
    quit_msg = small_font.render("ESC para salir", True, (220, 220, 220))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 332))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 370))
    screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, 405))


# ---------------------------
# Generación de enemigos
# ---------------------------
def spawn_enemy(enemies, difficulty_level):
    """Genera un enemigo en un carril aleatorio con velocidad creciente según el nivel."""
    if len(enemies) >= MAX_ACTIVE_ENEMIES:
        return False

    lane_order = list(range(LANE_COUNT))
    random.shuffle(lane_order)

    for lane in lane_order:
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
        base_speed = 4.2 + (difficulty_level * 0.35)
        enemy_speed = random.uniform(base_speed, base_speed + 1.4)
        enemies.append(EnemyCar(lane, y, random.choice(ENEMY_COLORS), speed=enemy_speed))
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
    score = 0.0
    difficulty_level = 1
    is_game_over = False
    return player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, score, difficulty_level, is_game_over


# ---------------------------
# Función principal del juego
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Escape")
    clock = pygame.time.Clock()

    high_score = load_high_score()
    player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, score, difficulty_level, is_game_over = reset_game()
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
                    player, enemies, road_scroll_y, spawn_timer, next_spawn_delay, score, difficulty_level, is_game_over = reset_game()

        if not is_game_over:
            # La puntuación aumenta con el tiempo para reflejar distancia recorrida.
            score += dt * BASE_SCORE_RATE
            difficulty_level = get_difficulty_level(score)

            # La carretera se mueve con un desplazamiento ligeramente mayor a medida que sube la dificultad.
            road_scroll_y = (road_scroll_y + SCROLL_SPEED + (difficulty_level - 1) * 0.08) % 120

            # Movimiento del jugador siguiendo la misma mecánica que antes
            keys = pygame.key.get_pressed()
            player.update(keys)

            # Generación aleatoria de enemigos con tiempo de espera variable
            spawn_timer += dt
            if spawn_timer >= next_spawn_delay:
                if spawn_enemy(enemies, difficulty_level):
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(1.0, 2.2)
                else:
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(0.6, 1.3)

            # Actualización de enemigos y eliminación cuando salen de la pantalla
            for enemy in enemies[:]:
                enemy.update()
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
                    spawn_timer = 0.0
                    next_spawn_delay = random.uniform(0.8, 2.0)

                if player.rect.colliderect(enemy.rect):
                    is_game_over = True
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    break

        # Dibujo del juego
        draw_background(screen, road_scroll_y)
        draw_hud(screen, score, high_score, difficulty_level, is_game_over)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        if is_game_over:
            draw_game_over(screen, score, high_score)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
