# 🌈 歇后语大挑战 🎯

一个基于 NiceGUI 的双人对战歇后语游戏，包含 14,032 条中国传统歇后语数据。

## 🎮 游戏特色

- 🎯 **双人竞技模式** - 两名玩家同时进行，各自答题
- 🎪 **丰富的歇后语库** - 包含 14,032 条传统中国歇后语
- 🎨 **精美的界面设计** - 采用现代化的彩色渐变设计
- 🎭 **个性化玩家名** - 支持自定义玩家名称，带有可爱emoji表情
- ⚡ **多种游戏轮数** - 支持 1轮、3轮、6轮、12轮、18轮等多种选择
- 🎊 **胜利庆祝动画** - 获胜时有炫酷的彩带动画庆祝
- 📱 **响应式设计** - 适配各种屏幕尺寸，界面紧凑美观
- 🔄 **完善的重置功能** - 一键重置游戏设置和玩家名称

## 🚀 快速开始

### 系统要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd xiehouyu_game
```

2. **安装依赖**
```bash
uv sync
```

3. **运行游戏**
```bash
uv run python xiehouyu_game.py
```

4. **打开浏览器**
游戏将在 `http://localhost:8080` 启动，浏览器会自动打开

## 🎯 游戏玩法

### 基本规则

1. **开始游戏** - 选择游戏轮数，点击"开始游戏"
2. **双人答题** - 两名玩家各自获得不同的歇后语题目
3. **选择答案** - 从4个选项中选择正确的后半句
4. **计分规则** - 答对得分，答错不得分
5. **胜负判定** - 游戏结束后得分高者获胜

### 游戏特色

- 🎪 **独立题目** - 每轮每位玩家获得不同的歇后语题目
- 🎯 **无时间限制** - 玩家可以仔细思考，不受时间压力
- 🎨 **实时反馈** - 答题后立即显示正确答案
- 🎊 **连击系统** - 连续答对可以获得连击记录
- 🎭 **个性化** - 支持自定义玩家名称和表情

## 📁 项目结构

```
xiehouyu_game/
├── xiehouyu_game.py        # 主游戏应用
├── game_logic.py           # 游戏逻辑核心
├── game_ui.py              # 用户界面组件
├── xiehouyu_explorer.py    # 数据探索工具
├── xiehouyu.json           # 歇后语数据集
├── test_game.py            # 游戏测试脚本
├── demo_usage.py           # 使用示例
├── pyproject.toml          # 项目配置
├── uv.lock                 # 依赖锁定文件
├── data/                   # 数据目录
├── ai_docs/                # AI文档资料
└── README.md               # 项目说明
```

## 🔧 开发指南

### 核心组件

- **GameState** - 游戏状态管理
- **GameUI** - 用户界面控制
- **PlayerPanel** - 玩家面板组件
- **GameOverDialog** - 游戏结束对话框
- **XiehouyuExplorer** - 数据探索工具

### 主要功能

1. **游戏逻辑** (`game_logic.py`)
   - 游戏状态管理
   - 回合进度控制
   - 计分系统
   - 题目生成

2. **用户界面** (`game_ui.py`)
   - 玩家面板
   - 答题界面
   - 胜利庆祝动画
   - 响应式布局

3. **数据管理** (`xiehouyu_explorer.py`)
   - 歇后语数据加载
   - 搜索和统计功能
   - 随机题目生成

### 自定义配置

你可以通过修改 `game_logic.py` 中的 `GameConfig` 类来自定义游戏设置：

```python
config = GameConfig(
    total_rounds=12,      # 默认轮数
    points_per_correct=1  # 每题得分
)
```

## 🎨 界面预览

游戏采用现代化的渐变色设计：
- 🔵 **玩家一** - 蓝绿色渐变面板
- 🟠 **玩家二** - 橙黄色渐变面板
- 🎊 **胜利庆祝** - 彩带动画和金色光效
- 📱 **响应式** - 适配不同屏幕尺寸

## 🌟 数据集说明

项目包含 14,032 条精选的中国传统歇后语，数据来源于 [chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua) 开源项目，涵盖：
- 生活常识类
- 历史典故类
- 动物植物类
- 谐音双关类
- 民间智慧类

数据格式：
```json
{
  "riddle": "八仙过海",
  "answer": "各显神通"
}
```

## 🛠️ 技术栈

- **后端框架**: [NiceGUI](https://nicegui.io/) - 现代化的Python Web UI框架
- **包管理**: [uv](https://docs.astral.sh/uv/) - 快速的Python包管理器
- **前端样式**: CSS3 渐变和动画
- **数据存储**: JSON 格式的歇后语数据集

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎯 双人对战功能
- 🎨 精美UI界面
- 🎊 胜利庆祝动画
- 📱 响应式设计

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢 [chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua) 项目提供的歇后语数据集
- 感谢所有贡献传统中国歇后语文化的前辈
- 感谢 [NiceGUI](https://nicegui.io/) 提供的优秀Web UI框架
- 感谢开源社区的支持和贡献

## 📞 联系方式

如果你有任何问题或建议，请通过以下方式联系：
- 创建 [Issue](../../issues)
- 提交 [Pull Request](../../pulls)

---

**让我们一起传承中华文化，在游戏中学习传统智慧！** 🎉