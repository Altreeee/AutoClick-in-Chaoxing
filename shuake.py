import pyautogui
import time
import gc
import itertools
import pyscreenshot #import pyscreenshot as ImageGrab
import threading
#D:
#cd D:/desktop/shua
#pyinstaller --onefile --hidden-import gc --hidden-import pyautogui --hidden-import time --hidden-import itertools shuake.py


# 等待程序开始，可以自己调整等待时间
time.sleep(10)

# 定义需要检测的图片
target_image = 'green_circle.png'   #播放完毕
next_episode_image = 'circle_2.png' #下一集
choices_image = 'option.png'  #选择题
confirm_image = 'confirm.png'  #确认
sidebar_location = (1900, 300) # 右侧边栏的位置，根据实际情况修改
confidence_threshold = 0.8 # 相似度阈值

def click_all_options(option_count):#暂时无法运行
    try:
        #生成选项数列表
        num = range(1, option_count+1)#1,2,3
        #生成所有可能的选项数组合
        num_combinations = []
        for i in range(1, len(num) + 1):
            for subset in itertools.combinations(num, i):
                num_combinations.append(subset)
        #num_combinations = [(1,), (2,), (3,), (1,2), (1,3), (2,3),(1,2,3)]每个元素是一个元组
        #生成匹配项列表
        options = list(set(pyautogui.locateAllOnScreen('option.png',confidence=0.8)))
        #确定选项数组合
        for combination in num_combinations:#(1,), (2,), (3,), (1,2), (1,3), (2,3),(1,2,3)
            #尝试每个选项                            |
            for number in combination:     #1/2 in (1,2)，每循环一次点击一个选项组和中的选项
                #查找所有匹配的选项点击                    
                location = options[number-1]#从匹配列表中找到当前位置的图片
                if not location:
                    break
                center = pyautogui.center(location)
                pyautogui.click(center)
                time.sleep(1)
            #选项组合点击完毕

            #点击继续播放
            location = pyautogui.locateOnScreen('confirm.png',confidence=0.8)
            if not location:
                break
            center = pyautogui.center(location)
            pyautogui.click(center)
            time.sleep(1)
    except Exception as e:
        # 发生异常，输出错误信息
        print(e)

def getcount():
    try:
        options = list(pyautogui.locateAllOnScreen('option.png',confidence=0.8))
        option_count = len(options)
        return option_count
    except Exception as e:
        # 发生异常，输出错误信息
        print(e)
    
def click():
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

def take_screenshot():
    im = pyscreenshot.grab()
    return im.tobytes()

def main2():
    screenshot1 = take_screenshot()
    while True:
        time.sleep(300)  # 5 minutes
        screenshot2 = take_screenshot()
        if screenshot1 != screenshot2:#屏幕改变
            screenshot1 = screenshot2
        else:#屏幕没变
            click()
        
        gc.collect()
    
def main1():
    while True:
        try:
            location = pyautogui.locateOnScreen(confirm_image, confidence=0.8)
            if location:    #如果存在“确认”键
                option_count = getcount()
                click_all_options(option_count)

            click()
            
            gc.collect()
            time.sleep(180)
        except Exception as e:
            # 发生异常，输出错误信息
            print(e)
        # 释放内存
        del location
    
if __name__ == '__main__':
    # Create two threads for each main function
    thread1 = threading.Thread(target=main1)
    thread2 = threading.Thread(target=main2)
    
    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
            
        

