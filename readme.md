# mnist

直接运行.ipynb, 加载数据，可视化，分割数据集，训练，评估性能，没什么可说的

# sudoku

直接运行sudoku_puzzle.py, 测试样例写好了，输出也很简单

# maze

这个就烦人了，非要搞什么可视化

1、运行maze.py，自动生成一个迷宫（10*15大小）

2、交互以修改设置（启用了pyplot的交互模式）

​	a、命令行询问 contiue modification?(y/n): ，y进行修改地图，n退出修改
​	b、如果a中选择了y，命令行询问 contiue modification?block(int int):2空格3，左下角为0 0，右上为 14 9，选择空方块就是封死它，选择蓝色块就是清空它，错了不要紧，直接就忽略了
​	c、重复a和b，除非用n在a中退出了
​	d、后面会选择出发点和终点，start position(int int):0 0，destination position(int int): 3 3，选了蓝色格不要紧，有检测，但是记得选有解的始点（橙色）和终点（绿色）
​	e、等他运行出结果，变化的灰色箭头是这个位置（state）采取行动（action）的可视化，箭头越长，Q值越大（越倾向于采取这个action），最后解出来路径是棕色的，和灰色箭头趋势一致，最后命令行提示：随便输入点什么就可以退出了
​	

