# Leo's Desktop Buddy

A tiny, transparent Windows companion that runs toward the mouse pointer. When he
catches it, Leo playfully fights it with a punch-and-kick combo. Move the pointer
away and he immediately resumes the chase. Leo is always on top but click-through,
so he never blocks clicks or typing.

## Build the executable on Windows

1. Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/windows/).
2. Double-click `build-windows.bat`.
3. Send `dist\LeoDesktopBuddy.exe` to Leo.

No installer or administrator rights are required. The executable is portable:
double-click it to start and use the blue tray icon's **Exit** item to stop it.
Windows SmartScreen may show an "unrecognized app" message because this personal
build is not code-signed; choose **More info → Run anyway** if you trust the file.

## Optional GitHub build

The included GitHub Actions workflow builds the same `.exe` on a Windows runner.
After pushing the repository, run **Build Windows app** from the Actions tab and
download the `LeoDesktopBuddy-Windows` artifact.

## Privacy

The finished app is entirely local. It does not use the network, record the screen,
or collect mouse activity; it only reads the current cursor coordinates so Leo can
follow them. The reference photo is not bundled into the executable.
