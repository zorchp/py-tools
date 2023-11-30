import time

sum = 10  # 设置倒计时时间
interval = 0.25  # 设置屏幕刷新的间隔时间
for i in range(0, int(sum / interval)):
    list = ["\\", "|", "/", "-"]
    index = i % 4
    print("\r程序正在运行 {}".format(list[index]), end="")
    time.sleep(interval)
