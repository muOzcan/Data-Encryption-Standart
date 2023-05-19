
from key_scheduler import key_scheduler
from encrypt import encrypt
from encrypt import _ascii_to_bin
from decrypt import decrypt




düzMetin = "simetrik anahtarlama"
print("__________________________________________________\n")
print("Düz Metin : " + düzMetin + "\n")
print("Düz Metin Binary: " + _ascii_to_bin(düzMetin) + "\n")
print("Düz Metin Hexadecimal: " + hex(int(_ascii_to_bin(düzMetin), 2   ))+"\n")


anahtarlar = key_scheduler(10870162528230930430)
sifreliMetin = encrypt(düzMetin, anahtarlar)


print("__________________________________________________\n")
print("Şifreli Metin : " + sifreliMetin + "\n")
print("Şifreli Metin Hexadecimal: " + hex(int(sifreliMetin, 2)))


print("__________________________________________________\n")
sifresiCozulmusMetin = decrypt(sifreliMetin, anahtarlar)
print(sifresiCozulmusMetin.encode("utf-8"))


