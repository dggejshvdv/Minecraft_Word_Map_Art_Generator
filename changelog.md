# Changelog | 更新日志

## v1.0.0-pre2 (2026-07-21)

### New Features | 新增功能

**System Font Support | 系统字体支持**
- Now supports reading fonts installed on the system automatically | 自动读取系统已安装的字体
- No longer required to place font files in the ttf/ directory | 无需将字体文件放在ttf/目录
- Users just need to install fonts by double-clicking font files | 用户只需双击字体文件安装即可
- Searches system font directories on Windows, macOS, and Linux | 支持Windows、macOS、Linux系统字体目录

**Preview Window | 预览窗口**
- Added file list view showing all generated .litematic files | 添加文件列表视图显示所有生成的投影文件
- Double-click any file to open a new preview window | 双击文件打开新的预览窗口
- Two preview modes available: | 两种预览模式：
  - Map Art Preview: Shows pixel-based map art (default) | 地图画预览：显示像素化地图画（默认）
  - 2D Build Preview: Shows blocks with textures, supports mouse drag and zoom | 建造预览(2D)：显示带材质的方块，支持鼠标拖拽和缩放

**Texture Support | 材质支持**
- Preview renders using Minecraft texture files from assets/minecraft/textures/block | 使用Minecraft材质文件进行预览渲染
- Users can copy the assets folder from Minecraft jar file to the project root | 用户可从Minecraft jar文件复制assets文件夹到项目根目录
- Supports textures for concrete, wool, carpet, and terracotta blocks | 支持混凝土、羊毛、地毯、陶瓦材质  
- Falls back to solid colors if textures are not available | 材质不可用时回退到纯色渲染

**Settings Menu (设置) | 设置菜单**
- Added Settings menu item in the top menu bar | 在顶部菜单栏添加设置菜单项
- Click Settings to directly open settings dialog | 点击设置直接打开设置窗口
- Language menu separated into independent menu item | 语言菜单独立为栏中的一个项
- Settings and Language menu items show both Chinese and English | 设置和语言菜单项显示中英文
- New settings dialog for configuring: | 新增设置对话框，可配置：
  - Default block type (Concrete by default) | 默认方块类型（默认混凝土）
  - Default preview mode (Map Art by default) | 默认预览方式（默认地图画）
  - Default font (Empty by default) | 默认字体（默认无）
- Settings are saved to config.json file | 设置保存到config.json文件
- config.json contains both settings and language configuration | config.json包含设置和语言配置两部分

### Improvements | 改进与优化

**UI Layout | UI布局**
- Replaced preview area with generated files list | 将预览区域替换为生成文件列表
- Generated files list shows existing .litematic files on startup | 启动时自动加载已有的投影文件
- Files are added to the list as they are generated | 文件生成时自动添加到列表

**File Management | 文件管理**
- Settings are persisted between sessions | 设置在会话间持久化保存
- Font list now includes both system fonts and custom ttf/ directory fonts | 字体列表包含系统字体和自定义ttf/目录字体

### Documentation Updates | 文档更新

- Updated Chinese documentation `README/README zh_cn.md` | 更新中文文档
- Updated English documentation `README/README en.md` | 更新英文文档
- Added `changelog.md` | 添加更新日志

---

## v1.0.0-pre1 (2026-07-19)

### New Features | 新增功能

**Graphical User Interface | 图形界面**
- Added GUI built with PyQt6 | 新增基于PyQt6的图形界面
- Supports font selection, text input, color selection, symbol selection | 支持字体选择、文字输入、颜色选择、符号选择
- Real-time log output display | 实时日志输出显示

**Internationalization Support | 国际化支持**
- Added i18n framework supporting Chinese and English | 新增i18n框架，支持中文和英文
- Auto-detects system language on first launch | 首次启动自动检测系统语言
- Language can be switched from the top-right corner | 界面右上角支持切换语言

**Color Selection Panel | 颜色选择面板**
- 16 Minecraft concrete colors as visual buttons, click to select color | 16个Minecraft混凝土颜色可视化按钮，点击选择

**Symbol Selection Panel | 符号选择面板**
- Categorized common symbols (punctuation, quotes, parentheses, math symbols, etc.) | 分类展示常用符号（标点、引号、括号、数学符号等）
- Click symbols to insert directly into input field | 点击符号直接插入输入框

**Clear Log Button | 清除日志按钮**
- Added clear log button at the top of log area | 日志区域顶部新增清除日志按钮
- One-click to clear log content | 一键清空日志内容

### Improvements | 改进与优化

**Project Refactoring | 项目重构**
- Separated core logic into `main.py` | 将核心逻辑分离到main.py
- GUI separated into `ui.py` | 图形界面独立为ui.py
- i18n framework separated into `i18n.py` | 国际化框架独立为i18n.py
- Translation files stored in `i18n/` directory | 翻译文件统一存放于i18n/目录

**Directory Structure | 目录结构**
- Auto-creates `ttf/`, `litematic/` directories on startup | 运行时自动创建ttf/、litematic/目录
- README documents stored in `README/` directory | README文档统一存放于README/目录

**CLI Mode Removed | 命令行模式移除**
- No longer provides command-line functionality | 不再提供命令行功能
- Must be launched via `ui.py` | 只能通过ui.py启动程序

**Log Optimization | 日志优化**
- Simplified log output format, removed redundant information | 简化日志输出格式，移除冗余信息

### Documentation Updates | 文档更新

- Updated Chinese documentation `README/README zh_cn.md` | 更新中文文档
- Added English documentation `README/README en.md` | 新增英文文档
- Updated project structure and usage instructions | 更新项目结构说明和使用方法