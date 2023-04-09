import pyautogui
import time
import gc
#pyinstaller --onefile --hidden-import pyautogui --hidden-import time shuake.py

# 等待程序开始，可以自己调整等待时间
time.sleep(5)

# 定义需要检测的图片
target_image = 'green_circle.png'
next_episode_image = 'circle_2.png'
sidebar_location = (1900, 300) # 右侧边栏的位置，根据实际情况修改
confidence_threshold = 0.8 # 相似度阈值

while True:
    try:
        # 尝试在屏幕上查找目标图片
        location = pyautogui.locateOnScreen(target_image, confidence=confidence_threshold)
        if location:
            # 找到目标图片，点击右侧边栏中的下一集按钮
            next_episode_location = pyautogui.locateOnScreen(next_episode_image, confidence=0.95)
            
            if next_episode_location:
                # 找到下一集按钮，点击
                pyautogui.click(x=1782,y=next_episode_location[1])
            else:
                # 没有找到下一集按钮，移动鼠标到边栏中心位置，再滚动滚轮向下
                pyautogui.moveTo(sidebar_location)
                pyautogui.scroll(-100)
                
            # 等待一段时间，避免误操作
            time.sleep(5)
            pyautogui.click(x=473,y=939)   
        
        gc.collect()
        time.sleep(300)
    except Exception as e:
        # 发生异常，输出错误信息
        print(e)
    # 释放内存
    del location
