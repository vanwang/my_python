import pyautogui
import time

# 预留几秒时间切换到印象笔记窗口
print("请在 3 秒内切换到印象笔记窗口...")
time.sleep(3)

# 按钮坐标与尺寸（根据截图估算）
button = {"x": 20, "y": 70, "width": 150, "height": 40}

# 计算按钮的中心点（点击更稳定）
center_x = button["x"] + button["width"] // 2
center_y = button["y"] + button["height"] // 2

# 移动鼠标到按钮中心并点击
pyautogui.moveTo(center_x, center_y, duration=0.5)  # 平滑移动到按钮位置
pyautogui.click()

print("✅ 已自动点击『新建笔记』按钮")
pyautogui.alert('This is an alert box.')
