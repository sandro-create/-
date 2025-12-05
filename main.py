import pygame      # 提供遊戲所需功能
import random      # 處理隨機數字
# import time      # <-- Pygbag 兼容環境下，我們使用 pygame.time.get_ticks() 替代 time.time()
import sys         # 控制退出程式
import asyncio     # <-- 【重點新增】用於 Web 環境的非同步處理

# 初始化
pygame.init()

# 顯示窗口的像素大小
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("點數字")

# 會用到的顏色的設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FIRST_BOX = (150, 150, 150)
SECOND_BOX = (180, 180, 180)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# 字型的設定
# 注意：在 Pygbag 環境中，最好使用 font.SysFont("dejavusans", 50) 或加載自定義字體
# 為了兼容性，我們建議使用一個已知的字體，這裡暫時保持 None 測試
font = pygame.font.SysFont(None, 50) 

# 5*5的格子大小
grid_size = 5
cell_size = WIDTH // grid_size

# 遊戲狀態變數 (全局變數)
numbers = []
next_numbers = []
current = 1
start_time_ms = 0  # 【修改】使用毫秒 (milliseconds) 計時
game_over = False
elapsed = 0
result_text = ""

# ----------------------------------------------------
# 函數定義
# ----------------------------------------------------

def draw_grid():
    """畫出 5x5 方格與數字"""
    
    for i in range(grid_size):
        for j in range(grid_size):
            num = numbers[i * grid_size + j]
            
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            
            if num != 0:
                # 根據數字決定顏色
                if num <= 25:
                    color = FIRST_BOX
                else:
                    color = SECOND_BOX

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 3)

                # 顯示數字
                text = font.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)


def show_message(text, color=WHITE, y_offset=0):
    """設定一個函式，可以把想顯示的字打出來"""
    
    msg = font.render(text, True, color)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(msg, rect)


def reset_game():
    """設定一個函式把遊戲所有狀態回到一開始的樣子"""
    
    global numbers, next_numbers, current, start_time_ms, game_over, result_text, elapsed
    
    numbers = list(range(1, 26))
    random.shuffle(numbers)
    next_numbers = list(range(26, 51))
    random.shuffle(next_numbers)
    
    current = 1
    start_time_ms = 0
    game_over = False
    result_text = ""
    elapsed = 0


# ----------------------------------------------------
# 主程式：包裹在 async 函式中
# ----------------------------------------------------

async def main(): # <-- 【重點修改】使用 async 定義主函式
    global current, start_time_ms, game_over, result_text, elapsed
    
    # 第一次啟動時先重置遊戲，確保變數初始化
    reset_game() 

    running = True

    while running:
        # 主迴圈開始時，先清空畫面
        screen.fill(BLACK) 

        # --- 事件處理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # 在 Pygbag 中，建議設定 running=False 讓迴圈結束
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row = y // cell_size
                col = x // cell_size
                index = row * grid_size + col
                
                if 0 <= index < 25:
                    num = numbers[index]

                    if num == current:
                        
                        if current == 1:
                            # 【修改】使用 pygame.time.get_ticks() 獲取遊戲運行毫秒數
                            start_time_ms = pygame.time.get_ticks() 

                        if num <= 25:
                            if next_numbers:
                                numbers[index] = next_numbers.pop(0)
                            else:
                                numbers[index] = 0
                        else:
                            numbers[index] = 0

                        current += 1

                        if current > 50:
                            # 【修改】使用 pygame.time.get_ticks() 獲取結束時間
                            end_time_ms = pygame.time.get_ticks() 
                            # 計算花費時間，轉換為秒
                            elapsed = round((end_time_ms - start_time_ms) / 1000, 2)
                            game_over = True
                            result_text = f"You spend {elapsed} seconds!"
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                
                if event.key == pygame.K_q:
                    # 在 Web 環境中，K_q 建議也只是結束遊戲循環
                    running = False


        draw_grid() # 每一幀都重畫整個 5×5 格子

        # --- 計時器顯示 (可選，但建議保留) ---
        if start_time_ms != 0 and not game_over:
            # 顯示當前時間
            current_time_ms = pygame.time.get_ticks()
            time_spent = round((current_time_ms - start_time_ms) / 1000, 1)
            time_text = font.render(f"Time: {time_spent}", True, WHITE)
            screen.blit(time_text, (10, 10))


        if game_over:
            # 如果 game_over == True，生成結算畫面
            for i in range(grid_size):
                for j in range(grid_size):
                    # for 迴圈把畫面塗成全黑
                    rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, BLACK, rect)
            
            show_message(result_text, WHITE)
            show_message("Press R/Q Restart/Quit", GREEN, 50)
        
        pygame.display.update()

        # 【關鍵步驟】釋放控制權給瀏覽器
        await asyncio.sleep(0) 

    # 迴圈結束後，安全退出
    pygame.quit()
    sys.exit()

# ----------------------------------------------------
# 啟動程式 (在本地和 Web 環境中啟動)
# ----------------------------------------------------

if __name__ == "__main__":
    # 使用 asyncio 運行主函式
    try:
        asyncio.run(main())
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass