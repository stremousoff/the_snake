from random import randint

import pygame

pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
OUTLINE_COLOR = (93, 216, 228)

# Скорость движения змейки
SPEED = 8

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """GameObject — это базовый класс, от которого наследуются другие игровые
    объекты.
    """

    def __init__(self):
        """Конструктор класса GameObject."""
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = None

    @staticmethod
    def draw(body_color, position):
        """Это абстрактный метод, который предназначен для переопределения
        в дочерних классах. Этот метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """
        rect = pygame.Rect((position[0], position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, 1)


class Apple(GameObject):
    """Класс унаследованный от GameObject, описывающий яблоко
    и действия с ним.
    """

    def __init__(self):
        """Конструктор класса Apple."""
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    @staticmethod
    def randomize_position():
        """Устанавливает случайное положение яблока на игровом поле."""
        return (
            randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
            randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
        )

    def draw(self, *args):
        """Отрисовывает яблоко на игровой поверхности."""
        super().draw(self.body_color, self.position)


class Snake(GameObject):
    """Класс унаследованный от GameObject, описывающий змейку
    и действия с ней.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = self.position
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_position = self.get_head_position()
        x_point = head_position[0]
        y_point = head_position[1]

        if x_point >= SCREEN_WIDTH:
            x_point = - GRID_SIZE
        elif x_point < 0:
            x_point = SCREEN_WIDTH

        if y_point >= SCREEN_HEIGHT:
            y_point = - GRID_SIZE
        elif y_point < 0:
            y_point = SCREEN_HEIGHT

        if self.direction == RIGHT:
            self.positions.insert(0, (x_point + GRID_SIZE, y_point))
        elif self.direction == LEFT:
            self.positions.insert(0, (x_point - GRID_SIZE, y_point))
        elif self.direction == UP:
            self.positions.insert(0, (x_point, y_point - GRID_SIZE))
        elif self.direction == DOWN:
            self.positions.insert(0, (x_point, y_point + GRID_SIZE))

        self.last = self.positions.pop()

    def draw(self, *args):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            super().draw(self.body_color, position)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, OUTLINE_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения
        с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл программы."""
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        apple.draw()
        snake.draw()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple = Apple()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple = Apple()
        pygame.display.update()


if __name__ == '__main__':
    main()
