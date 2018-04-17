local bit = require("bit")

-- openwrt lua5.1 不支持位操作 menuconfig add lua bitop module

function encrypt(key, s)
    local band, bor, bxor = bit.band, bit.bor, bit.bxor
    local lshift, rshift, rol = bit.lshift, bit.rshift, bit.rol
    n = string.len(s)  -- 求出s的字节数
    c = ""
    j = 0
    for i = 1, n, 1 do
        b1 = string.byte(s, i) -- char to int
        --b2 = b1 ~ key -- b1 = b2^ key
        b2 = bxor(b1, key)
        c1 = b2 % 16
        -- c2 = b2 // 16 -- b2 = c2*16 + c1
        c2 = rshift(b2, 4)
        c1 = c1 + 65
        c2 = c2 + 65  -- c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c = c .. string.char(c1) .. string.char(c2)
    end
    return c
end

key = 15
local uptime=assert (io.popen("macd5.sh"))
sn = uptime:read("*l")
print(sn)
uptime:close()

print(encrypt(key, sn))

