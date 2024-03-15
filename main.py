import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Definir colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Pelea")

# Cargar imagen de fondo
imagen_fondo = pygame.image.load("fondo.jpg")  # Cambiar por la ruta de tu archivo JPG
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Clase para representar a un personaje
class Personaje(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vida = 1000

    def update(self, dx, dy):
        # Comprobar límites de la pantalla
        if 0 <= self.rect.x + dx <= ANCHO - self.rect.width:
            # Comprobar si se está moviendo hacia la izquierda
            if dx < 0:
                self.rect.x += dx
            # Comprobar si se está moviendo hacia la derecha
            elif dx > 0:
                self.rect.x += dx

        if 0 <= self.rect.y + dy <= ALTO - self.rect.height:
            # Comprobar si se está moviendo hacia arriba
            if dy < 0:
                self.rect.y += dy
            # Comprobar si se está moviendo hacia abajo
            elif dy > 0:
                self.rect.y += dy

# Cargar imágenes para los personajes
imagen_personaje1 = "pikachu.png"  # Cambiar por la ruta de tu archivo PNG
imagen_personaje2 = "charmander.png"  # Cambiar por la ruta de tu archivo PNG

# Crear los personajes
pikachu = Personaje(imagen_personaje1, 100, 100)
charmander = Personaje(imagen_personaje2, 600, 100)

# Grupo de sprites para manejar los personajes
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(pikachu)
todos_los_sprites.add(charmander)

# Definir rectángulos para las barras de vida
ancho_barra_vida = 200
alto_barra_vida = 20
barra_vida_pikachu = pygame.Rect(10, 10, ancho_barra_vida, alto_barra_vida)
barra_vida_charmander = pygame.Rect(ANCHO - ancho_barra_vida - 10, 10, ancho_barra_vida, alto_barra_vida)

# Fuente para mostrar los puntos de vida
fuente = pygame.font.Font(None, 30)

# Variables para controlar los disparos
disparos_pikachu = []
disparos_charmander = []

# Estado del juego
game_over = False

# Bucle principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Pikachu dispara al presionar la tecla Espacio
                disparos_pikachu.append(pygame.Rect(pikachu.rect.x + pikachu.rect.width, pikachu.rect.y + pikachu.rect.height // 2 - 5, 20, 10))
            elif event.key == pygame.K_RETURN:
                # Charmander dispara al presionar la tecla Enter
                disparos_charmander.append(pygame.Rect(charmander.rect.x, charmander.rect.y + charmander.rect.height // 2 - 5, 20, 10))

    # Capturar el estado de las teclas para el movimiento de los personajes
    keys = pygame.key.get_pressed()
    # Movimiento de Pikachu
    if keys[pygame.K_a]:
        pikachu.update(-5, 0)
    if keys[pygame.K_d]:
        pikachu.update(5, 0)
    if keys[pygame.K_w]:
        pikachu.update(0, -5)
    if keys[pygame.K_s]:
        pikachu.update(0, 5)
    # Movimiento de Charmander
    if keys[pygame.K_LEFT]:
        charmander.update(-5, 0)
    if keys[pygame.K_RIGHT]:
        charmander.update(5, 0)
    if keys[pygame.K_UP]:
        charmander.update(0, -5)
    if keys[pygame.K_DOWN]:
        charmander.update(0, 5)

    # Actualizar posición de los disparos de Pikachu
    for disparo in disparos_pikachu:
        disparo.x += 10  # Velocidad del disparo
        # Verificar si el disparo golpea a Charmander
        if disparo.colliderect(charmander.rect):
            charmander.vida -= 50  # Reducir la vida de Charmander en 50
            disparos_pikachu.remove(disparo)

    # Actualizar posición de los disparos de Charmander
    for disparo in disparos_charmander:
        disparo.x -= 10  # Velocidad del disparo
        # Verificar si el disparo golpea a Pikachu
        if disparo.colliderect(pikachu.rect):
            pikachu.vida -= 50  # Reducir la vida de Pikachu en 50
            disparos_charmander.remove(disparo)

    # Verificar si alguno de los personajes ha perdido toda su vida
    if pikachu.vida <= 0 or charmander.vida <= 0:
        game_over = True

    # Limpiar la pantalla
    pantalla.fill(NEGRO)

    # Dibujar el fondo
    pantalla.blit(imagen_fondo, (0, 0))

    # Dibujar los disparos de Pikachu
    for disparo in disparos_pikachu:
        pygame.draw.rect(pantalla, ROJO, disparo)

    # Dibujar los disparos de Charmander
    for disparo in disparos_charmander:
        pygame.draw.rect(pantalla, ROJO, disparo)

    # Dibujar los personajes
    todos_los_sprites.draw(pantalla)

    # Dibujar las barras de vida
    #pygame.draw.rect(pantalla, NEGRO, barra_vida_pikachu)
    pygame.draw.rect(pantalla, ROJO, (barra_vida_pikachu.x + 1, barra_vida_pikachu.y + 1, pikachu.vida / 10, alto_barra_vida - 2))
    #pygame.draw.rect(pantalla, NEGRO, barra_vida_charmander)
    pygame.draw.rect(pantalla, ROJO, (barra_vida_charmander.x + 90, barra_vida_charmander.y + 1, charmander.vida / 10, alto_barra_vida - 2))

    # Mostrar los puntos de vida
    texto_pikachu = fuente.render(f"Vida: {pikachu.vida}", True, BLANCO)
    pantalla.blit(texto_pikachu, (barra_vida_pikachu.x + 10, barra_vida_pikachu.y + 30))
    texto_charmander = fuente.render(f"Vida: {charmander.vida}", True, BLANCO)
    pantalla.blit(texto_charmander, (barra_vida_charmander.x + 10, barra_vida_charmander.y + 30))

    # Verificar si el juego ha terminado
    if game_over:
        # Mostrar mensaje de "GAME OVER" con fondo negro
        game_over_texto = fuente.render("GAME OVER", True, BLANCO)
        game_over_rect = game_over_texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        pygame.draw.rect(pantalla, NEGRO, game_over_rect)
        pantalla.blit(game_over_texto, game_over_rect)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(30)

# Salir del juego después de 3 segundos
pygame.time.delay(3000)
pygame.quit()
sys.exit()
