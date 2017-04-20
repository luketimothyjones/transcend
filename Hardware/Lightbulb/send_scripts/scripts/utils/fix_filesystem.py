from flashbdev import bdev
uos.VfsFat.mkfs(bdev)
vfs = uos.VfsFat(bdev, "")

import machine
machine.reset()