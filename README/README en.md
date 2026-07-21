# Minecraft Word Map Art Generator

A tool for generating Minecraft map art projection files, supporting rendering text into 128×128 giant tiled map art using the Litematica mod for construction.

## Features

- 16 Minecraft colored blocks: Concrete, Wool, Carpet, Terracotta
- System Font Support: Automatically reads fonts installed on the system, no need to manually place font files
- Batch Generation: Input multiple characters at once, each generates a separate projection file
- Symbol Chinese Naming: Automatically converts symbols to Chinese names (e.g., `©` → `版权符号`)
- Corner Positioning: Special symbols automatically placed at map corners (e.g., `©®™` at top-right, `★☆` at top-left)
- Auto Directory Creation: Automatically creates `ttf/` and `litematic/` directories on startup
- Graphical Interface: Modern GUI built with PyQt6 for easier operation
- Multi-language Support: Chinese and English, auto-detects system language
- File Preview: Double-click generated projection files to open preview window
- Two Preview Modes: Map Art Preview, 2D Build Preview
- Texture Rendering: Supports Minecraft texture files for preview
- Settings: Configure default block type, default preview mode, default font

## Installation

### Requirements

- Python 3.8+
- Dependencies: `freetype-py`, `Pillow`, `litemapy`, `PyQt6`

### Install Dependencies

```bash
pip install freetype-py Pillow litemapy PyQt6
```

### Font Preparation

No need to manually place font files! The tool automatically reads fonts installed on the system. Users just need to install fonts by double-clicking font files.

### Texture Preparation (Optional)

To use texture rendering for preview, extract textures from Minecraft jar file:

1. Find the version jar file in your Minecraft directory (e.g., `1.21.jar`)
2. Open the jar file with an archive tool
3. Copy the `assets` folder to the project root directory
4. Ensure the path is: `assets/minecraft/textures/block/`

Supported texture files:
- `*_concrete.png` - Concrete textures
- `*_wool.png` - Wool textures
- `*_carpet.png` - Carpet textures
- `*_terracotta.png` - Terracotta textures

## Usage

### Launch the Program

```bash
python ui.py
```

### Workflow

1. Select Font: Choose a font from the dropdown menu (system-installed fonts)
2. Input Text: Enter the text or symbols to generate (supports multiple characters)
3. Select Block Type: Choose block type from dropdown (Concrete, Wool, Carpet, Terracotta)
4. Select Color: Click a color button to choose the text color
5. Insert Symbols: Click symbols from the symbol panel to insert directly
6. Generate: Click the "Generate Projection File" button
7. Preview: Double-click files in the right-side file list to open preview window

### Preview Function

After generating projection files, double-click files in the file list to open the preview window:

- **Map Art Preview**: Shows pixel-based map art style (default)
- **2D Build Preview**: 2D rendering with block textures, supports mouse wheel zoom and drag pan

**Preview Controls**:

- **Left-click drag**: Pan the view
- **Mouse wheel**: Zoom the view (centered at mouse position)
- **Toolbar buttons**: Zoom in, Zoom out, Reset view

### Settings

Click "设置 (Settings)" from the top menu bar to directly open the settings window:

- **Default Block Type**: Set the default block type on startup (Concrete, Wool, Carpet, Terracotta)
- **Default Preview Mode**: Set the default preview mode in preview window (Map Art, 2D)
- **Default Font**: Set the default font on startup

Settings are saved in `config.json` file, which contains both settings and language configuration.

### Log Output Example

```
Starting generation of 4 map art files...
[1/4] Generating: '你'
  Success! Projection file: litematic/AaZhuNiWoMingMeiXiangChunTian-2_你_Concrete_红色_1234.litematic
  Block count: 1234

[2/4] Generating: '好'
  Success! Projection file: litematic/AaZhuNiWoMingMeiXiangChunTian-2_好_Concrete_红色_1567.litematic
  Block count: 1567

[3/4] Generating: '世'
  Success! Projection file: litematic/AaZhuNiWoMingMeiXiangChunTian-2_世_Concrete_红色_1100.litematic
  Block count: 1100

[4/4] Generating: '界'
  Success! Projection file: litematic/AaZhuNiWoMingMeiXiangChunTian-2_界_Concrete_红色_1345.litematic
  Block count: 1345

============================================================
Generation complete! Generated 4 files
Total block count: 5246
============================================================
```

### Color Abbreviations

| Color      | Abbr | English      |
| ---------- | ---- | ------------ |
| White      | W    | white        |
| Orange     | O    | orange       |
| Magenta    | M    | magenta      |
| Light Blue | LB   | light\_blue  |
| Yellow     | Y    | yellow       |
| Lime       | L    | lime         |
| Pink       | P    | pink         |
| Gray       | Gy   | gray         |
| Silver     | S    | silver       |
| Cyan       | C    | cyan         |
| Purple     | V    | purple       |
| Blue       | B    | blue         |
| Brown      | Br   | brown        |
| Green      | G    | green        |
| Red        | R    | red          |
| Black      | Bl   | black        |

### Block Types

| Type | English | Description |
| --- | --- | --- |
| Concrete | concrete | Standard concrete block |
| Wool | wool | Wool block |
| Carpet | carpet | Wool carpet (half height) |
| Terracotta | terracotta | Terracotta block |

## In-Game Usage

1. Place the generated `.litematic` file in `.minecraft/schematics` folder
2. Install the **Litematica** mod in-game (requires MaLiLib)
3. Open the projection menu with a stick and load the file
4. Place the projection in the map area to build

## Project Structure

```
.
├── ui.py                                  # Graphical Interface (PyQt6)
├── main.py                                # Core Logic Module
├── i18n.py                                # Internationalization Framework
├── config.json                            # Configuration File (auto-generated)
├── assets/                                # Minecraft Textures Directory (optional)
│   └── minecraft/
│       └── textures/
│           └── block/                     # Block texture files
├── i18n/                                  # Translation Files Directory
│   ├── zh_cn.json                         # Chinese Translation
│   └── en.json                            # English Translation
├── ttf/                                   # Font Files Directory (optional)
├── litematic/                             # Projection Files Output Directory
└── README/
    ├── README zh_cn.md                        # Chinese Documentation
    └── README en.md                           # English Documentation
```

## File Descriptions

### ui.py

Main graphical interface program built with PyQt6, includes:
- Top menu bar (Settings, Language)
- Font selection dropdown
- Text input field
- Block type selector
- Color selection panel (16 colors)
- Symbol selection panel (categorized common symbols)
- Generated files list (double-click to preview)
- Output log display area
- Clear log button

### main.py

Core logic module responsible for:
- Font support checking
- System font searching
- Text rendering to image
- Image conversion to Litematica projection file
- Supports multiple block types (Concrete, Wool, Carpet, Terracotta)

**Note**: `main.py` no longer provides CLI mode, must be launched via `ui.py`.

### i18n.py

Internationalization framework supporting:
- Auto-detection of system language
- Runtime language switching
- JSON format translation files

### settings.json

Settings file that saves user configuration:
- Default block type
- Default preview mode
- Default font

## Technical Details

### File Naming Format

`FontName_Character_BlockType_Color_BlockCount.litematic`

Example: `AaZhuNiWoMingMeiXiangChunTian-2_你_Concrete_红色_1234.litematic`

### Corner Symbol Positions

| Symbols | Position   |
| ------- | ---------- |
| `©®™`   | Top-Right  |
| `°★☆`   | Top-Left   |
| `§`     | Bottom-Right|
| `●○`    | Bottom-Left|

### Font Support Checking

The tool uses `freetype-py` to check if the font supports input characters. If a character is not supported, it will prompt the user to re-enter.

### Language Switching

- Auto-detects system preferred language on first launch
- Language can be switched in "语言 (Language)" menu from the top menu bar (Chinese/English)
- Interface text updates immediately after switching

## License

MIT License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.

## Notes

- Font files must be prepared and installed by the user, ensure proper usage rights
- Generated map art is 128×128 blocks, requires sufficient building space
- Recommended to build in a superflat world or the End void for easier map coordinate alignment
- Texture files must be extracted from Minecraft jar file by the user, the tool does not provide any texture files

## Contributing

Contributions are welcome! Feel free to submit Issues and Pull Requests.