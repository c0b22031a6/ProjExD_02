import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1000, 550


delta = {  #練習3:押下キーと移動量の辞書 
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数rct:こうかとんor爆弾SurfaceのRect
    戻り値:横方向,縦方向はみ出し判定結果(画面内:True/画面外:False)
    """

    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0) 
    kk_rct = kk_img.get_rect()  # 練習3:こうかとんのRectを抽出する
    kk_rct.center = 800, 400  # 練習3:こうかとんの初期座標
    bb_img = pg.Surface((20,20))  # 練習1:透明のSurface
    bb_img.set_colorkey((0, 0, 0))  # 練習1:黒い部分を透明
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１：赤い半径10の円を描く  
    bb_rct = bb_img.get_rect()  # 練習1:爆弾のRectを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習2:爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    num1 = 100  # 追加機能3を実装するために設定
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            num1 = 0  #こうかとんが爆弾にぶつかったときにnum1を0にする
        num1 += 1  # num1を１ずつプラスする
        if num1 == 2:
            print("Game Over")
            return

        if num1 < 2:  # num1が２未満まで画像を切り替える
            kk_img = pg.image.load("ex02/fig/6.png")  # 画像切り替え
            kk_img = pg.transform.rotozoom(kk_img,0,2.0) 
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        """""  # 追加機能１の途中
        if sum_mv == [-5,0]:  # 各移動量の合計タプルの時の画像をif文で挿入しようとした
            kk_img = pg.transform.rotozoom(kk_img, 0, 1.0) 
        if sum_mv == [-5,-5]:
            kk_img1 = pg.transform.rotozoom(kk_img, 315, 1.0)
        if sum_mv == [0,-5]:
            kk_img2 = pg.transform.rotozoom(kk_img, 270, 1.0)
        if sum_mv == [+5,-5]:
            kk_img3 = pg.transform.rotozoom(kk_img, 225, 1.0)
        if sum_mv == [+5,0]:
            kk_imgs = pg.transform.flip(kk_img, True, True)
        if sum_mv == [+5,+5]:
            kk_img5 = pg.transform.rotozoom(kk_img, 135, 1.0)
        if sum_mv == [0,+5]:
            kk_img6 = pg.transform.rotozoom(kk_img, 90, 1.0)
        if sum_mv == [-5,+5]:
            kk_img7 = pg.transform.rotozoom(kk_img, 45, 1.0)
        """
        

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct) 
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)      


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()