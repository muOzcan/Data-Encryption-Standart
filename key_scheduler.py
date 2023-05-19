#!/usr/bin/env python

import random

"""
DES Key Scheduler:

- Rastgele oluşturulmuş 64 bitlik bir başlangıç anahtarından 16 adet 48 bitlik alt anahtar oluşturur
- İkili diziler biçiminde 16 adet alt anahtarın bir listesini döndürür

"""

def key_scheduler(k):

    # -------------------- Değişkenler -------------------- #
    #
    # k         Başlangıçtaki 64-bitlik anahtar
    # k_prime   Permutasyon yapılarak elde edilmiş 56-bitlik anahtar
    # c0        k_prime anahtarının sol parçası
    # d0        k_prime anahtarının sağ parçası
    # c_keys    c0'ın permütasyonları alınarak elde edilmiş 16 adet 28-bitlik anahtarlar
    # d_keys    d0'ın permütasyonları alınarak elde edilmiş 16 adet 28-bitlik anahtarlar
    # keys      Final 16 adet 48-bitlik anahtar
    #
    # --------------------------------------------------- #

    
    # ---------------- Hard-Coded Values ---------------- #

    # Permütasyon Tablosu 1
    # Bu tabloya göre 56-bitlik bloktaki her bir bitin yerleri değiştirilir
    # Örneğin, 57. biti 1. sıraya, 49. biti 2. sıraya, 41. biti 3. sıraya ...
    pc1 = [57, 49, 41, 33, 25, 17,  9,
            1, 58, 50, 42, 34, 26, 18,
           10,  2, 59, 51, 43, 35, 27,
           19, 11,  3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
           14,  6, 61, 53, 45, 37, 29,
           21, 13,  5, 28, 20, 12,  4]

    # Permütasyon Tablosu 2
    # Bu tabloya göre 56-bitlik bir bit dizisi 48-bitlik bir diziye indirgenir
    # Örneğin, 56-bitlik dizi cat olsun, bu durumda cat dizisinin 14.biti alınarak 1.sıraya, 17.biti alınarak 2. sıraya, ...
    # 32. biti alınarak 48. sıraya konulur ve böylece 48-bitlik bir blok elde edilmiş olur
    pc2 = [14, 17, 11, 24,  1,  5,
           3,  28, 15,  6, 21, 10,
           23, 19, 12,  4, 26,  8,
           16,  7, 27, 20, 13,  2,
           41, 52, 31, 37, 47, 55,
           30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53,
           46, 42, 50, 36, 29, 32]
           

    # lrt (left rotation table) : sol döndürme tablosu
    lrt = [1, 1, 2, 2, 2, 2, 2, 2,
           1, 2, 2, 2, 2, 2, 2, 1]

    # --------------------------------------------------- #


    

    # Rastgele 64 bit sayı oluşturur ve k'ya atanır
    # Not - Algoritma 64 bitlik bir anahtarla başlasa da DES teknik olarak hala 56-bit
    # Çünkü bitlerin 8'i parity biti olarak kullanılıyor. Bu bitler işlem sırasında kaybolur.
    # k = random.getrandbits(64)
    k = bin(k)[2:].zfill(64)
    

    # Permütasyon tablosu 1 (pc1) kullanılarak ilk ikame işlemi yapılır ve
    # k_prime elde edilir
    k_prime = ""
    for konum in pc1:
        k_prime += k[konum-1]
        

    # k_prime anahtarı sol ve sağ parçalara ayrılır
    # c_0 : sol 28-bitlik parça
    # d_0 : sağ 28 bitlik parça
    c0 = k_prime[:28]
    d0 = k_prime[28:]


    # lrt (sol döndürme tablosuna) göre c0 ve d0 parçaları 16 tur boyunca döndürülür
    # Bu tabloya göre her turda lrt tablosundaki sayı kadar bit c0 ve d0 bitlerinin sağına doğru kaydırılır
    # Örneğin, c0=1001011...0 olsun. tur0'da lrt[0]=1 ise, döngü sonunda c0=001011...01 olur. 
    # Örneğin, d0=0110010...1 olsun. tur2'de lrt[2]=2 ise, döngü sonunda d0=10010...101 olur.
    # Böylece, her iki parçada yapılan değişiklikler ile elde edilen yeni parçalar c_anahtarlar ve d_anahtarlar listesine eklenir
    c_anahtarlar = []
    d_anahtarlar = []
    for i in range(16):
        num = lrt[i]

        temp = c0[0:num]
        c0 = c0[num:] + temp
        c_anahtarlar.append(c0)

        temp = d0[0:num]
        d0 = d0[num:] + temp
        d_anahtarlar.append(d0)


    # c_anahtarlar[i] ve d_anahtarlar[i] sol ve sağ parçalarının birleştirilmesi ile 16 adet 56-bitlik alt anahtar elde edilir
    # 56-bitlik anahtarlardan 48-bitlik anahtarlar elde etmek için ise pc2 tablosu kullanılır
    # pc2 tablosunda belirtilen konumlar cat bit dizisinden seçilir ve yeni 48-bitlik alt anahtar elde edilmiş olur
    # Böylece 16 adet 48-bitlik alt anahtarlar üretilmiş olur
    altAnahtarlar = []
    for i in range(16):
        cat = c_anahtarlar[i] + d_anahtarlar[i]
        temp = ""
        for konum in pc2:
            temp += cat[konum-1]
        altAnahtarlar.append(temp)

        

        
    return altAnahtarlar




