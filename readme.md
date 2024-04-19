# Ideapad2024 Power Management

Manage power settings for the Lenovo Ideapad 2024 (IdeaPad Pro 5 (Gen 9)) with the CLI tool `ideapad2024-power-manage`, alongside a system tray icon for convenient access.

## Description

This package provides a command-line interface (CLI) tool and a system tray application to manage power settings on the Lenovo Ideapad 2024. It allows users to adjust performance modes and battery conservation settings easily. Remember, you'll need to manually start the tray by executing `ideapad2024-power-tray`.

## Installation

To install the `ideapad2024-power-management` package, follow these steps:

1. Have a basic understanding of how Arch PKGBUILD works, that means, you can read and understand the PKGBUILD file.
2. Clone the repository or download the package source.
3. Navigate to the directory containing the package.
4. If you are using Arch-based distros, run `makepkg -si` to build and install the package. or go to AUR and install the package from there.
5. If you are using other distros, please read the PKGBUILD file and install the dependencies manually.

Please note that the package conflicts with `power-profiles-daemon`, so you may need to remove that package before installing.

## Usage

After installation, you can manage your power settings using the following commands:

- **Check current power status**: `ideapad2024-power-manage -c`
- **Set battery mode**: `ideapad2024-power-manage -b {conserve,normal,rapid}`
- **Set performance mode**: `ideapad2024-power-manage -p {performance,extreme,powersave}`

To access a system tray icon for convenient power management, run `ideapad2024-power-tray`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributions

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements or bug fixes.





## Appendix

### How to update .SRCINFO

```bash
makepkg --printsrcinfo > .SRCINFO
```



### How to install it locally

```bash
makepkg -sif
```

