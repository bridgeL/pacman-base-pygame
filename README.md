# pacman
based on pygame

## core
纯逻辑模块，不涉及任何具体的绘制，因此与pygame完全解耦

其中所有坐标均使用行、列顺序，原点为左上角， 位置也使用高、宽顺序

## draw

负责将core中逻辑坐标映射到pygame的绘制函数中（需要翻转行列）

添加绘画时的偏置（美观）

## 说明
逻辑与渲染分离，便于升级或更换渲染引擎，便于代码的移植

# 已知的问题

1. 逃跑算法的终态总是位于四个角落，显得很呆

2. 复活后，怪物如果仍处于惧怕状态，且吃豆人在上方，则怪物会躲在房子里不出来

3. 只有一只怪物，一种追逐逻辑

4. 怪物可以穿越边界去追逐玩家，但是这份写法不具有通用性，仅可适配该地图，是一种 bad code

# 特性

- 怪物采用a*寻路
- 直观展示怪物寻路路线
- 可以通过1-7快捷键调整mover移动速度
- 可以预存储一次转向指令，避免玩家在岔路口总是拐不进去
- 可以通过鼠标中键瞬移pacman
- 可以通过鼠标右键切换pacman的强力形态
- 可以使用r快捷重开
- 可以使用空格暂停游戏
- 支持小键盘、wasd、ijkl控制

