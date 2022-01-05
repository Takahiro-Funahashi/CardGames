import glob
import logging
import logging.handlers
import numpy as np
import os
import pygame


class GameCommon():
    def __init__(self):
        """ 初期化
        """

        self.card_number = [
            'ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
            'jack', 'queen', 'king'
        ]
        self.suit_key = ['spades', 'hearts', 'clubs', 'diamonds']

        self.init_logger()

        return

    def init_logger(self):
        path = os.getcwd() + '/log'
        if not os.path.exists(path):
            os.makedirs(path)

        self.hLog = logging.getLogger(__name__)
        self.hLog.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        hFile = logging.handlers.RotatingFileHandler(
            filename=path+'\game_log.log',
            maxBytes=3*1024*1024,
            backupCount=3,
            encoding='utf-8',
        )
        hFile.setLevel(logging.DEBUG)
        hFile.setFormatter(formatter)
        self.hLog.addHandler(hFile)

        return

    def init_pygeme(self, title_name='Card Games'):
        """ PyGame(GUI)初期化
        """

        pygame.init()
        self.game_screen = pygame.display.set_mode(
            size=self.screen_size,
            # flags=pygame.FULLSCREEN,
        )
        pygame.display.set_caption(title_name)

        self.game_font = pygame.font.Font(
            None, self.font_size)

        return

    def draw_background(self, color='darkgreen'):
        """ 背景描画
        """

        self.game_screen.fill(color)
        return

    def load_card_image(self):
        self.card_image = dict()

        card_path = os.getcwd() + \
            '/source/card_asset/playing-cards-assets/png/'

        if os.path.exists(card_path):
            for suit in self.suit_key:
                search_result = glob.glob(
                    card_path + f'*{suit}.png'
                )
                if search_result:
                    set_dict = dict()
                    for s in search_result:
                        file_name = os.path.basename(s)
                        label = file_name.replace(f'_of_{suit}.png', '')
                        img = pygame.image.load(s)
                        img = pygame.transform.scale(img, self.card_size)
                        set_dict.setdefault(label, img)
                        # self.game_screen.blit(img, (0, 0))
                    self.card_image.setdefault(suit, set_dict)
            backgound_key = ['background', 'backside']
            for back in backgound_key:
                search_result = glob.glob(
                    card_path + f'*{back}.png'
                )
                if search_result:
                    set_dict = dict()
                    for s in search_result:
                        file_name = os.path.basename(s)
                        img = pygame.image.load(s)
                        img = pygame.transform.scale(img, self.card_size)
                        set_dict.setdefault(back, img)
                    self.card_image.setdefault(back, set_dict)
        else:
            err_msg = 'The specified path does not exist.'
            self.hLog.error(err_msg)
            raise err_msg

        return

    def event_pygame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                break
            # マウスボタンクリック
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 左ボタンクリック
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_left_clicked(event)
                # 右ボタンクリック
                elif event.button == pygame.BUTTON_RIGHT:
                    self.mouse_right_clicked(event)
            # マウスボタンリリース
            if event.type == pygame.MOUSEBUTTONUP:
                # 左ボタンリリース
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_left_release(event)
                # 右ボタンリリース
                elif event.button == pygame.BUTTON_RIGHT:
                    self.mouse_right_release(event)
            # マウスモーション
            if event.type == pygame.MOUSEMOTION:
                self.mouse_move_on(event)
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel(event)

    def quit(self):
        pygame.quit()

    def mouse_left_clicked(self, event):
        x, y = event.pos
        return

    def mouse_right_clicked(self, event):
        x, y = event.pos
        return

    def mouse_left_release(self, event):
        x, y = event.pos
        return

    def mouse_right_release(self, event):
        x, y = event.pos
        return

    def mouse_move_on(self, event):
        x, y = event.pos
        return

    def mouse_wheel(self, event):
        print('wheel:', event.x, event.y)
        return


class Concentration(GameCommon):
    def __init__(self):
        """ 初期化
        """
        super().__init__()

        W, H = 0, 1

        self.offset_x, self.offset_y = 30, 30
        self.space = 15

        # トランプ札の定義
        self.suit = 4
        self.suit_num = 13

        self.card_size = (120, 180)

        # ボードサイズ
        x = (self.offset_x * 2) + \
            (self.card_size[W]+self.space) * self.suit_num - self.space
        y = (self.offset_y * 2) + \
            (self.card_size[H]+self.space) * self.suit + self.space*10
        self.screen_size = x, y
        # フォントサイズ
        self.font_size = 24

        # Geme Title
        self.title_name = "Concentration"

        # 手数
        self.efforts = 0
        return

    def init_game(self):

        # np.random.randintを使用すると、同じ数字が入ってしまう。

        tmp_array = np.arange(self.suit*self.suit_num)
        np.random.shuffle(tmp_array)
        self.card_array = np.reshape(tmp_array+1, (self.suit_num, self.suit))

        self.turned_card_array = np.full((self.suit_num, self.suit), 1)
        self.display_card_array = np.full((self.suit_num, self.suit), np.nan)

        return

    def draw_card(self):
        isRet, isWait = False, False

        W, H = 0, 1

        draw_array = self.card_array*self.turned_card_array
        draw_index = np.where(draw_array != 0)

        disp_card = np.where(np.logical_not(np.isnan(self.display_card_array)))
        self.card_object = list()

        if draw_index:
            raw, clm = draw_index
            screen = self.game_screen
            img_backside_card = self.card_image['backside']['backside']

            for x_index, y_index in zip(raw, clm):
                x = self.offset_x + (self.card_size[W]+self.space)*x_index
                y = self.offset_y + (self.card_size[H]+self.space)*y_index
                self.card_object.append(screen.blit(img_backside_card, (x, y)))

        if disp_card:
            raw, clm = disp_card
            screen = self.game_screen

            comb_card = dict()

            for x_index, y_index in zip(raw, clm):
                x = self.offset_x + (self.card_size[W]+self.space)*x_index
                y = self.offset_y + (self.card_size[H]+self.space)*y_index

                card_index = self.display_card_array[x_index, y_index]-1
                suit_index = int(card_index/self.suit_num)
                card_num_index = int(card_index % self.suit_num)

                img_back_card = self.card_image['background']['background']
                self.card_object.append(screen.blit(img_back_card, (x, y)))

                suit = self.suit_key[suit_index]
                card_number = self.card_number[card_num_index]

                card_img = self.card_image[suit][card_number]
                self.card_object.append(screen.blit(card_img, (x, y)))
                if card_num_index not in comb_card:
                    comb_card.setdefault(card_num_index, [(x_index, y_index)])
                else:
                    comb_card[card_num_index].append((x_index, y_index))
            if comb_card:
                for clist in comb_card.values():
                    if len(clist) == 2:
                        for x_index, y_index in clist:
                            self.display_card_array[x_index, y_index] = np.nan
                        isWait = True
                        self.efforts += 1
                    else:
                        if len(comb_card) > 1:
                            for x_index, y_index in clist:
                                self.display_card_array[x_index,
                                                        y_index] = np.nan
                                self.turned_card_array[x_index, y_index] = 1
                            isWait = True
                            self.efforts += 1

                isRet = True

        # GUI描画更新
        pygame.display.update()

        if isWait:
            pygame.time.delay(1000)

        return isRet

    def run(self):
        """ 神経衰弱画面の実行ループ
        """

        self.load_card_image()

        self.isLoop = True

        # カード配列初期化
        self.init_game()

        self.isInit = True
        while(self.isLoop):
            if self.isInit:
                # GUI画面初期化
                self.init_pygeme(self.title_name)
                # 背景描画
                self.draw_background()

                if not self.judge_game_over():
                    self.isInit = self.draw_card()

            # GUIイベント処理
            self.event_pygame()

        return

    def quit(self):
        pygame.quit()
        self.isLoop = False

        return

    def mouse_left_clicked(self, event):
        select_card = None
        for i, card in enumerate(self.card_object):
            if card.collidepoint(event.pos):
                select_card = i, card
                break

        if select_card is not None:
            W, H = 0, 1

            index, card = select_card
            x_pos = card.x-self.offset_x+self.card_size[W]/2
            y_pos = card.y-self.offset_y+self.card_size[H]/2
            x_unit = self.card_size[W]+self.space
            y_unit = self.card_size[H]+self.space
            x_index = int(x_pos/x_unit)
            y_index = int(y_pos/y_unit)
            self.turned_card_array[x_index, y_index] = 0
            self.display_card_array[x_index, y_index] = \
                self.card_array[x_index, y_index]

            self.isInit = True

        return

    def judge_game_over(self):
        ans1 = np.any(self.turned_card_array == 1)
        ans2 = np.any(np.logical_not(np.isnan(self.display_card_array)))
        if not ans1 and not ans2:
            print('GameOver:', self.efforts)
            self.quit()


class CardGames(GameCommon):
    def __init__(self):
        """ 初期化
        """
        super().__init__()

        # ボードサイズ
        self.screen_size = 300, 400

        # フォントサイズ
        self.font_size = 32

        self.title_manu = [
            "Concentration",
            "Exit",
        ]

        return

    def draw_title_menu(self):
        self.hLog.debug('Started "Card Games".')

        W, H = 0, 1
        offset_h = 20
        space = 15
        self.bottm_size = self.screen_size[W]*0.9, 30
        screen = self.game_screen

        self.title_bottom = dict()

        for i, text in enumerate(self.title_manu):
            set_dict = dict()
            sy = offset_h + space*i + self.bottm_size[H]*i
            sx = (self.screen_size[W]-self.bottm_size[W])/2
            w = self.bottm_size[W]
            h = self.bottm_size[H]

            rect = pygame.draw.rect(
                surface=screen,
                color='gray',
                rect=(sx, sy, w, h),
                width=0
            )

            set_dict.setdefault('Rect', rect)

            char = self.game_font.render(text, True, 'black')
            tw, th = self.game_font.size(text)

            tx = sx+(self.bottm_size[W]-tw)/2
            ty = sy+(self.bottm_size[H]-th)/2

            screen.blit(char, [tx, ty])

            set_dict.setdefault('Text', char)

            self.title_bottom.setdefault(text, set_dict)

        return

    def run(self):
        """ タイトル画面の実行ループ
        """

        self.isLoop = True
        self.game_mode = 'title'
        isInit = True
        while(self.isLoop):
            if isInit:
                # GUI画面初期化
                self.init_pygeme()
                # 背景描画
                self.draw_background()

                self.draw_title_menu()
                # GUI描画更新
                pygame.display.update()

                isInit = False

            # GUIイベント処理
            self.event_pygame()

            if self.switch_game_mode():
                isInit = True

        return

    def quit(self):
        pygame.quit()
        self.isLoop = False

        return

    def mouse_left_clicked(self, event):
        if self.title_bottom:
            for key, val in self.title_bottom.items():
                rect = val['Rect']
                if rect:
                    if rect.collidepoint(event.pos):
                        self.game_mode = key
        return

    def switch_game_mode(self):
        mode = self.game_mode
        if mode in self.title_bottom:
            if mode == 'Exit':
                self.quit()
            elif mode == 'Concentration':
                pygame.quit()
                self.switch_Concentration()

            self.game_mode = 'title'

            return True

        return False

    def switch_Concentration(self):
        Concentration().run()
        return


if __name__ == '__main__':
    CardGames().run()
