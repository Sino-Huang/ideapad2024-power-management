# Maintainer: SinoCici <hsk6808065@163.com>
pkgname=ideapad2024-power-management
pkgver=0.0.1
pkgrel=1
pkgdesc="Manage power settings for the Lenovo Ideapad 2024 (IdeaPad Pro 5 (Gen 9)) with the CLI tool `ideapad2024-power-manage`, alongside a system tray icon for convenient access. Remember, you'll need to manually start the tray by executing `ideapad2024-power-tray`."
arch=("any")
url=""
license=("MIT")
conflicts=('power-profiles-daemon')
install="build.install"
depends=("python" "python-pyqt6" "cpupower" "acpi_call-dkms")
makedepends=()
provides=()
conflicts=()
source=("ideapad2024-power-manage.py" "ideapad2024-power-tray.py" "power_management.png" "99-acquire-acpi-permit.rules" "99-user-automatic-powermode.rules")
sha256sums=('33b85a324cf6b3a8c62dbf9be57c25216d6840b319280f35d45878a90a25bc3b'
            'a5ca61dbd093dc2b80fa9f0a4c8517c5f5175404abbe791603e132e78a736598'
            '2dd29c575513e67439ceaffaf4a7b61cb5aeb23e6ad41d0e309336bb7e997785'
            '849582c2061e7e6e6bc0ac66b714a4065a91da6b771639cb7163a87a0eb31d11'
            '521884c1256cb35d26cbb432dd12aa561138c9e4702e4ccecfdd1c91cb86e9a1')


build() {
	# at this point the user can still be captured by $(whoami)
	cd "$srcdir"
	# we need to put the following to the /etc/sudoers.d/01_$(whoami)_ideapad2024-power-management
	# $(whoami) ALL=(ALL) NOPASSWD: /usr/bin/cpupower frequency-set -g powersave
    # $(whoami) ALL=(ALL) NOPASSWD: /usr/bin/cpupower frequency-set -g schedutil

	pred="# editted by ideapad2024-power-management"
	l1="$(whoami) ALL=(ALL) NOPASSWD: /usr/bin/cpupower frequency-set -g powersave"
	l2="$(whoami) ALL=(ALL) NOPASSWD: /usr/bin/cpupower frequency-set -g schedutil"
	post="# end of editted by ideapad2024-power-management"

	echo $pred | sudo tee $srcdir/01_$(whoami)_ideapad2024-power-management
	echo $l1 | sudo tee -a $srcdir/01_$(whoami)_ideapad2024-power-management
	echo $l2 | sudo tee -a $srcdir/01_$(whoami)_ideapad2024-power-management
	echo $post | sudo tee -a $srcdir/01_$(whoami)_ideapad2024-power-management

	echo $(whoami) | tee $srcdir/whoami.txt

}

package() {
	# Note that $(whoami) is not available here
	username=$(cat "$srcdir/whoami.txt")
    cd "$srcdir"
	install -Dm 755 "$srcdir/ideapad2024-power-manage.py" "${pkgdir}/usr/bin/ideapad2024-power-manage"

	install -Dm 755 "$srcdir/ideapad2024-power-tray.py" "${pkgdir}/usr/bin/ideapad2024-power-tray"

	install -Dm 644 "$srcdir/power_management.png" "${pkgdir}/usr/share/${pkgname}/power_management.png"

	install -Dm 644 "$srcdir/99-acquire-acpi-permit.rules" "${pkgdir}/etc/udev/rules.d/99-acquire-acpi-permit.rules"

	install -Dm 644 "$srcdir/99-user-automatic-powermode.rules" "${pkgdir}/etc/udev/rules.d/99-user-automatic-powermode.rules"

	install -Dm 644 "$srcdir/01_${username}_ideapad2024-power-management" "${pkgdir}/etc/sudoers.d/01_${username}_ideapad2024-power-management"

	# modify acpi_call permission in the build.install script, otherwise it will not work because build and package are done in virtual environment
}
