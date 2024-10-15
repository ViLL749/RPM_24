import pygame
import random

pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Лабиринт')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# параметры стен и дверей
line_width = 10
line_gap = 40
line_offset = 20
door_width = 40  # Увеличиваем ширину двери
max_openings_per_line = 5

# параметры и стартовая позиция игрока
player_radius = 10
player_speed = 2
player_x = screen_width - 12
player_y = screen_height - line_offset

# Загрузка и масштабирование фонового изображения
background_image = pygame.image.load('background.jpg')  # Убедитесь, что файл существует
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# рисуем стены и двери
lines = []
for i in range(0, screen_width, line_gap):
    # Генерируем количество открытий в стене
    num_openings = random.randint(1, max_openings_per_line)
    # Определяем границы открытий
    openings = sorted(
        random.sample(range(line_offset + door_width, screen_height - line_offset - door_width), num_openings))

    # Создаем стены с дверями
    last_opening_bottom = 0
    for opening_top in openings:
        # Верхняя часть стены
        lines.append(pygame.Rect(i, last_opening_bottom, line_width, opening_top - last_opening_bottom))
        last_opening_bottom = opening_top + door_width
    # Нижняя часть стены
    lines.append(pygame.Rect(i, last_opening_bottom, line_width, screen_height - last_opening_bottom))


# Функция для отображения текста
def show_message(message):
    font = pygame.font.Font(None, 74)  # Шрифт и размер текста
    text = font.render(message, True, white)  # Создаем текстовое изображение
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))  # Центрируем текст
    screen.fill(black)  # Заливаем экран черным цветом
    screen.blit(text, text_rect)  # Рисуем текст на экране
    pygame.display.update()  # Обновляем экран
    pygame.time.delay(2000)  # Задержка, чтобы показать сообщение 2 секунды


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # передвижение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_radius:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen_width - player_radius:
        player_x += player_speed
    elif keys[pygame.K_UP] and player_y > player_radius:
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and player_y < screen_height - player_radius:
        player_y += player_speed

    # проверка столкновений игрока со стенами
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    collided = False

    for line in lines:
        if line.colliderect(player_rect):
            # Проверяем, если столкновение произошло со стеной
            if line.height > door_width:  # Если это не дверь
                collided = True
                # Обрабатываем столкновение
                if player_x < line.left:
                    player_x = line.left - player_radius  # Уходим влево
                elif player_x > line.right:
                    player_x = line.right + player_radius  # Уходим вправо
                elif player_y < line.top:
                    player_y = line.top - player_radius  # Уходим вверх
                elif player_y > line.bottom:
                    player_y = line.bottom + player_radius  # Уходим вниз
            else:
                # Если столкновение с дверью, игрок может пройти
                collided = False

    # Проверка столкновения с левой стеной
    if player_rect.colliderect(pygame.Rect(0, 0, line_width, screen_height)):
        show_message("Вы выиграли!")  # Показываем сообщение о выигрыше
        player_x = screen_width - 12  # Сбрасываем позицию игрока
        player_y = screen_height - line_offset

    if collided:
        show_message("Вы проиграли!")  # Показываем сообщение о проигрыше
        player_x = screen_width - 12  # Сбрасываем позицию игрока
        player_y = screen_height - line_offset

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка стен и игрока
    for line in lines:
        pygame.draw.rect(screen, green, line)
    pygame.draw.circle(screen, red, (player_x, player_y), player_radius)

    pygame.display.update()
    clock.tick(60)
