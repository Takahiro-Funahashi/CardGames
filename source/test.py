import glob
import pygame
import os

card_number = [
    'ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    'jack', 'queen', 'king'
]


class CardGames():
    def __init__(self):
        """ 初期化
        """

        # ボードサイズ
        self.screen_size = 600, 400

        # フォントサイズ
        self.font_size = 24

        self.cnt = 0

        return

    def init_pygeme(self):
        """ PyGame(GUI)初期化
        """

        pygame.init()
        self.game_screen = pygame.display.set_mode(
            size=self.screen_size,
            # flags=pygame.FULLSCREEN,
        )
        pygame.display.set_caption('ReversiAI')

        self.game_font = pygame.font.Font(
            None, self.font_size)

        return

    def run(self):
        """ ゲーム実行開始
        """

        self.init_pygeme()
        self.draw_background()
        self.load_card_image()

        # GUI描画更新
        pygame.display.update()

        isLoop = True
        while(isLoop):

            # GUIイベント処理
            if 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        isLoop = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            x, y = event.pos
                            self.draw_screen()
                            # GUI描画更新
                            pygame.display.update()
        return

    def draw_background(self):
        """ 背景描画
        """

        self.game_screen.fill('darkgreen')
        return

    def load_card_image(self):
        self.card_image = dict()

        card_path = os.getcwd() + \
            '/source/card_asset/playing-cards-assets/png/'
        suit_key = ['spades', 'hearts', 'clubs', 'diamonds']

        if os.path.exists(card_path):
            for suit in suit_key:
                search_result = glob.glob(
                    card_path + f'*{suit}.png'
                )
                if search_result:
                    set_dict = dict()
                    for s in search_result:
                        file_name = os.path.basename(s)
                        label = file_name.replace(f'_of_{suit}.png', '')
                        set_dict.setdefault(label, pygame.image.load(s))
                    self.card_image.setdefault(suit, set_dict)

        return

    def draw_screen(self):
        screen = self.game_screen

        self.cnt += 1

        pygame.draw.circle(
            surface=screen,
            color='black',
            center=(10+self.cnt*10, 10+self.cnt*10),
            radius=10
        )
        return


if __name__ == '__main__':
    CardGames().run()
