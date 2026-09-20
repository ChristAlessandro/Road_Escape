import os
import random
import pygame
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RETURN,
    K_RIGHT,
    K_r,
    K_UP,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

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
BUTTON_BG = (35, 43, 52)
BUTTON_SELECTED = (60, 105, 175)

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
BASE_SCORE_RATE = 12

# Estados del juego
STATE_MENU = "menu"
STATE_CONTROLS = "controls"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

# ---------------------------
# Sistema de archivos y sonido
# ---------------------------
def load_high_score():
    """Carga el récord guardado en un archivo local del proyecto."""
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            return max(0, int(file.read().strip()))
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    """Guarda el récord en disco para mantenerlo entre partidas."""
    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
        file.write(str(max(0, int(score))))


def load_sounds():
    """Carga sonidos si existen; si no, devuelve None sin romper el juego."""
    sounds = {
        "select": None,
        "collision": None,
    }

    sound_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds"))
    try:
        pygame.mixer.init()
    except pygame.error:
        return sounds

    for key, filename in {
        "select": "menu_select.wav",
        "collision": "collision.wav",
    }.items():
        path = os.path.join(sound_dir, filename)
        if os.path.exists(path):
            try:
                sounds[key] = pygame.mixer.Sound(path)
            except pygame.error:
                sounds[key] = None

    music_path = os.path.join(sound_dir, "background.ogg")
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.25)
        except pygame.error:
            pass

    return sounds


def play_sound(sounds, sound_name):
    """Reproduce un efecto si existe y está disponible."""
    if sounds.get(sound_name) is not None:
        sounds[sound_name].play()


def pause_music():
    """Pausa la música si existe."""
    if pygame.mixer.get_init() is not None and pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()


def resume_music():
    """Reanuda la música si existe."""
    if pygame.mixer.get_init() is not None and not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()


# ---------------------------
# Sistema de nivel y dificultad
# ---------------------------
def get_level(score):
    """Nivel infinito calculado por puntuación acumulada."""
    return 1 + int(score // 500)


def get_enemy_speed(level):
    """Velocidad base de los enemigos según el nivel actual."""
    return 4.2 + (level - 1) * 0.35


def get_spawn_delay(level):
    """Intervalo entre apariciones, más corto según aumenta la dificultad."""
    return max(0.65, 1.7 - (level - 1) * 0.06)


def get_max_active_enemies(level):
    """Cantidad máxima de enemigos activa en pantalla, acotada para jugar bien."""
    return min(4, 2 + (level // 4))


# ---------------------------
# Clase del vehículo del jugador
# ---------------------------
class PlayerCar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def update(self, keys, dt):
        """Mueve el auto con izquierda, derecha, adelante y atrás dentro de la carretera."""
        move_x = (keys[K_RIGHT] - keys[K_LEFT]) * PLAYER_SPEED
        move_y = (keys[K_DOWN] - keys[K_UP]) * PLAYER_SPEED

        self.rect.x += move_x * dt * 60
        self.rect.y += move_y * dt * 60

        road_left = (WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        playable_top = 60
        playable_bottom = HEIGHT - 25 - PLAYER_HEIGHT

        self.rect.x = max(road_left, min(self.rect.x, road_right - PLAYER_WIDTH))
        self.rect.y = max(playable_top, min(self.rect.y, playable_bottom))

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

    def update(self, dt):
        """Desplaza el enemigo hacia abajo con velocidad variable."""
        self.rect.y += self.speed * dt * 60

    def draw(self, screen):
        """Dibuja el enemigo con colores y detalles distintos."""
        draw_vehicle(screen, self.rect, self.color, is_player=False)


# ---------------------------
# Funciones de dibujo
# ---------------------------
def draw_vehicle(screen, rect, color, is_player):
    """Dibuja un auto con forma reconocible, manteniendo tamaño y hitbox actuales."""
    x, y, width, height = rect

    shadow = pygame.Rect(x + 4, y + 6, width, height)
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=14)

    body = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, body, border_radius=14)

    pygame.draw.rect(screen, tuple(max(0, c - 18) for c in color), (x + 7, y + 12, width - 14, height - 26), border_radius=12)

    window_color = (198, 220, 255) if is_player else (220, 224, 230)
    pygame.draw.rect(screen, window_color, (x + 10, y + 14, width - 20, 22), border_radius=6)
    pygame.draw.rect(screen, window_color, (x + 12, y + 38, width - 24, 16), border_radius=5)

    front_bumper = pygame.Rect(x + width - 6, y + 18, 6, height - 36)
    rear_bumper = pygame.Rect(x, y + 18, 6, height - 36)
    pygame.draw.rect(screen, (80, 80, 80), front_bumper, border_radius=3)
    pygame.draw.rect(screen, (80, 80, 80), rear_bumper, border_radius=3)

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

    if is_player:
        pygame.draw.rect(screen, (255, 255, 255), (x + 14, y + 16, width - 28, 3), border_radius=2)


def draw_background(screen, road_scroll_y):
    """Pinta el fondo, carretera y entorno lateral con movimiento visual."""
    screen.fill(BLACK)

    mountain_color = (28, 36, 50)
    for i in range(-20, WIDTH + 80, 90):
        pts = [(i, 220), (i + 30, 140), (i + 60, 220)]
        pygame.draw.polygon(screen, mountain_color, pts)

    road_left = (WIDTH - ROAD_WIDTH) // 2
    road_right = road_left + ROAD_WIDTH

    pygame.draw.rect(screen, ROAD_EDGE, (road_left - 28, 0, 28, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE, (road_right, 0, 28, HEIGHT))
    pygame.draw.rect(screen, ROAD_SURFACE, (road_left, 0, ROAD_WIDTH, HEIGHT))

    pygame.draw.rect(screen, ACCENT, (road_left - 2, 0, 2, HEIGHT))
    pygame.draw.rect(screen, ACCENT, (road_right, 0, 2, HEIGHT))

    lane_width = ROAD_WIDTH / LANE_COUNT
    for i in range(1, LANE_COUNT):
        lane_x = road_left + i * lane_width
        pygame.draw.line(screen, LANE_LINE, (lane_x, 0), (lane_x, HEIGHT), 3)

    stripe_height = 34
    stripe_width = 10
    for y in range(-60, HEIGHT + 60, 60):
        draw_y = (y + road_scroll_y) % (HEIGHT + 60)
        for i in range(LANE_COUNT - 1):
            lane_x = road_left + (i + 1) * lane_width
            pygame.draw.rect(screen, LANE_LINE, (lane_x - stripe_width // 2, draw_y, stripe_width, stripe_height), border_radius=3)

    side_color = (70, 90, 75)
    for offset in range(0, HEIGHT + 60, 90):
        y = (offset + road_scroll_y * 2) % (HEIGHT + 90)
        tree_x_left = road_left - 28
        tree_x_right = road_right + 18

        pygame.draw.rect(screen, (135, 135, 135), (tree_x_left, y + 8, 5, 22), border_radius=2)
        pygame.draw.rect(screen, side_color, (tree_x_left - 12, y, 18, 18), border_radius=9)
        pygame.draw.rect(screen, (120, 120, 120), (tree_x_right, y + 8, 5, 22), border_radius=2)
        pygame.draw.rect(screen, side_color, (tree_x_right - 6, y, 18, 18), border_radius=9)

    for y in range(0, HEIGHT + 40, 80):
        pygame.draw.rect(screen, (200, 200, 200), (road_left - 10, y, 6, 26), border_radius=3)
        pygame.draw.rect(screen, (200, 200, 200), (road_right + 4, y, 6, 26), border_radius=3)


def draw_button(screen, rect, text, selected):
    """Dibuja un botón simple para menú y pantallas auxiliares."""
    color = BUTTON_SELECTED if selected else BUTTON_BG
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)

    font = pygame.font.SysFont("arial", 24, bold=True)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))


def draw_menu(screen, high_score, selected_index):
    """Dibuja la pantalla principal con título, opciones y récord."""
    draw_background(screen, 0)

    title_font = pygame.font.SysFont("arial", 46, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 16)

    title = title_font.render("Road Escape", True, ACCENT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

    items = ["Jugar", "Controles", "Salir"]
    start_y = 250
    button_h = 52
    gap = 18

    for i, item in enumerate(items):
        rect = pygame.Rect(WIDTH // 2 - 120, start_y + i * (button_h + gap), 240, button_h)
        draw_button(screen, rect, item, selected_index == i)

    record_text = subtitle_font.render(f"Récord: {int(high_score)}", True, WHITE)
    screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 520))


def draw_controls(screen, selected_index):
    """Muestra la pantalla de controles con una opción para volver."""
    draw_background(screen, 0)

    title_font = pygame.font.SysFont("arial", 36, bold=True)
    text_font = pygame.font.SysFont("arial", 18)

    title = title_font.render("Controles", True, ACCENT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    lines = [
        "← → : mover izquierda / derecha",
        "↑ : mover hacia adelante",
        "↓ : mover hacia atrás",
        "ESC : pausar / continuar",
        "R : reiniciar tras Game Over",
    ]

    for index, line in enumerate(lines):
        label = text_font.render(line, True, WHITE)
        screen.blit(label, (90, 180 + index * 48))

    back_rect = pygame.Rect(WIDTH // 2 - 130, 530, 260, 52)
    draw_button(screen, back_rect, "Volver", selected_index == 0)


def draw_hud(screen, score, high_score, level, is_game_over):
    """Muestra la información principal sin cubrir la carretera."""
    panel = pygame.Rect(0, 0, WIDTH, 58)
    pygame.draw.rect(screen, HUD_BG, panel)

    title_font = pygame.font.SysFont("arial", 18, bold=True)
    info_font = pygame.font.SysFont("arial", 11)

    title = title_font.render("ROAD ESCAPE", True, TEXT_COLOR)
    score_text = info_font.render(f"Score: {int(score)}", True, ACCENT)
    record_text = info_font.render(f"Record: {int(high_score)}", True, WHITE)
    level_text = info_font.render(f"Nivel: {level}", True, (120, 220, 255))
    status = "RUNNING" if not is_game_over else "GAME OVER"
    status_text = info_font.render(status, True, ACCENT if not is_game_over else (255, 90, 90))

    screen.blit(title, (18, 12))
    screen.blit(score_text, (18, 34))
    screen.blit(record_text, (120, 34))
    screen.blit(level_text, (220, 34))
    screen.blit(status_text, (WIDTH - 100, 18))


def draw_pause_overlay(screen):
    """Muestra la pantalla de pausa con instrucciones para continuar."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("arial", 42, bold=True)
    info_font = pygame.font.SysFont("arial", 18)

    title = title_font.render("PAUSA", True, ACCENT)
    continue_text = info_font.render("ESC para continuar", True, WHITE)
    menu_text = info_font.render("M para volver al menú", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 45))


def draw_game_over(screen, score, high_score, level):
    """Muestra la pantalla de fin de partida con puntuación, récord y nivel."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    header = pygame.Rect(70, 210, WIDTH - 140, 220)
    pygame.draw.rect(screen, (30, 30, 35), header, border_radius=18)
    pygame.draw.rect(screen, (255, 90, 90), header, 2, border_radius=18)

    font_big = pygame.font.SysFont("arial", 42, bold=True)
    font_small = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)

    title = font_big.render("GAME OVER", True, (255, 110, 110))
    score_text = font_small.render(f"Puntuación: {int(score)}", True, WHITE)
    record_text = font_small.render(f"Récord: {int(high_score)}", True, ACCENT)
    level_text = font_small.render(f"Nivel: {level}", True, (120, 220, 255))
    restart = font_small.render("R para reiniciar", True, WHITE)
    menu_text = small_font.render("M para volver al menú", True, (220, 220, 220))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 235))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 295))
    screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 328))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 361))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 395))
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 425))


# ---------------------------
# Generación de enemigos
# ---------------------------
def spawn_enemy(enemies, level):
    """Genera un enemigo en un carril aleatorio con comprobación de espacio."""
    max_enemies = get_max_active_enemies(level)
    if len(enemies) >= max_enemies:
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
        speed = get_enemy_speed(level) + random.uniform(0, 1.2)
        enemies.append(EnemyCar(lane, y, random.choice(ENEMY_COLORS), speed=speed))
        return True

    return False


def reset_run():
    """Devuelve el estado inicial de una partida nueva."""
    road_left = (WIDTH - ROAD_WIDTH) // 2
    player = PlayerCar(road_left + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2), HEIGHT - 150)
    enemies = []
    road_scroll_y = 0
    score = 0.0
    level = 1
    spawn_timer = 0.0
    next_spawn_delay = 1.5
    is_game_over = False
    return player, enemies, road_scroll_y, score, level, spawn_timer, next_spawn_delay, is_game_over


def start_game():
    """Inicializa una partida nueva."""
    return reset_run()


# ---------------------------
# Función principal del juego
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Road Escape")
    clock = pygame.time.Clock()

    sounds = load_sounds()
    if pygame.mixer.get_init() is not None:
        try:
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    high_score = load_high_score()
    state = STATE_MENU
    selected_menu_index = 0
    selected_controls_index = 0

    player, enemies, road_scroll_y, score, level, spawn_timer, next_spawn_delay, is_game_over = start_game()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_music()
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING
                        resume_music()
                    elif state == STATE_CONTROLS:
                        state = STATE_MENU
                        selected_menu_index = 0
                        if sounds["select"] is not None:
                            sounds["select"].play()
                    elif state == STATE_GAME_OVER:
                        running = False

                if state == STATE_MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_menu_index = (selected_menu_index - 1) % 3
                        play_sound(sounds, "select")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_menu_index = (selected_menu_index + 1) % 3
                        play_sound(sounds, "select")
                    elif event.key in (K_RETURN, pygame.K_SPACE):
                        if selected_menu_index == 0:
                            player, enemies, road_scroll_y, score, level, spawn_timer, next_spawn_delay, is_game_over = start_game()
                            state = STATE_PLAYING
                            resume_music()
                            play_sound(sounds, "select")
                        elif selected_menu_index == 1:
                            state = STATE_CONTROLS
                            selected_controls_index = 0
                            play_sound(sounds, "select")
                        elif selected_menu_index == 2:
                            running = False

                elif state == STATE_CONTROLS:
                    if event.key in (K_RETURN, pygame.K_SPACE, K_ESCAPE):
                        state = STATE_MENU
                        selected_menu_index = 0
                        play_sound(sounds, "select")

                elif state == STATE_PAUSED:
                    if event.key in (pygame.K_m, pygame.K_M):
                        state = STATE_MENU
                        selected_menu_index = 0
                        resume_music()
                    elif event.key == K_ESCAPE:
                        state = STATE_PLAYING
                        resume_music()

                elif state == STATE_GAME_OVER:
                    if event.key == K_r:
                        player, enemies, road_scroll_y, score, level, spawn_timer, next_spawn_delay, is_game_over = start_game()
                        state = STATE_PLAYING
                        resume_music()
                    elif event.key in (pygame.K_m, pygame.K_M):
                        state = STATE_MENU
                        selected_menu_index = 0
                        resume_music()

                if state == STATE_PLAYING and event.key == pygame.K_p:
                    state = STATE_PAUSED
                    pause_music()

            elif event.type == MOUSEBUTTONDOWN and state == STATE_MENU:
                x, y = event.pos
                items = ["Jugar", "Controles", "Salir"]
                start_y = 250
                button_h = 52
                for index, _ in enumerate(items):
                    rect = pygame.Rect(WIDTH // 2 - 120, start_y + index * (button_h + 18), 240, button_h)
                    if rect.collidepoint(x, y):
                        selected_menu_index = index
                        if index == 0:
                            player, enemies, road_scroll_y, score, level, spawn_timer, next_spawn_delay, is_game_over = start_game()
                            state = STATE_PLAYING
                            resume_music()
                        elif index == 1:
                            state = STATE_CONTROLS
                        elif index == 2:
                            running = False
                        play_sound(sounds, "select")
                        break

        if state == STATE_PLAYING:
            score += dt * BASE_SCORE_RATE
            level = get_level(score)
            road_scroll_y = (road_scroll_y + SCROLL_SPEED + (level - 1) * 0.08) % 120

            keys = pygame.key.get_pressed()
            player.update(keys, dt)

            spawn_timer += dt
            if spawn_timer >= next_spawn_delay:
                if spawn_enemy(enemies, level):
                    spawn_timer = 0.0
                    next_spawn_delay = get_spawn_delay(level) + random.uniform(0.0, 0.5)
                else:
                    spawn_timer = 0.0
                    next_spawn_delay = max(0.5, get_spawn_delay(level) - 0.15)

            for enemy in enemies[:]:
                enemy.update(dt)
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
                    spawn_timer = 0.0
                    next_spawn_delay = get_spawn_delay(level) + random.uniform(0.2, 0.8)
                if player.rect.colliderect(enemy.rect):
                    play_sound(sounds, "collision")
                    is_game_over = True
                    state = STATE_GAME_OVER
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    break

        # Dibujo del juego
        if state == STATE_MENU:
            draw_menu(screen, high_score, selected_menu_index)
        elif state == STATE_CONTROLS:
            draw_controls(screen, selected_controls_index)
        elif state in (STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER):
            draw_background(screen, road_scroll_y)
            draw_hud(screen, score, high_score, level, state == STATE_GAME_OVER)
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)

            if state == STATE_PAUSED:
                draw_pause_overlay(screen)
            elif state == STATE_GAME_OVER:
                draw_game_over(screen, score, high_score, level)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
