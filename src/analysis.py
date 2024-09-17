import re
import matplotlib.pyplot as plt
import seaborn as sns

# 初始化数据列表
y_values = []

# 读取log.txt文件
with open('log.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 使用正则表达式匹配 "Total book count: " 后面的数字
        match = re.search(r'Total book count:\s*(\d+)', line)
        if match:
            # 提取数字并将其添加到y_values列表中
            y_values.append(int(match.group(1)))

# 绘制折线图
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# 绘制y值的折线图，x轴为序列索引
sns.lineplot(x=range(len(y_values)), y=y_values)

# 设置图表标题和轴标签
plt.title('Total Book Count Over Time')
plt.xlabel('Requests')
plt.ylabel('Total Book Count')

# 显示图表
plt.show()
