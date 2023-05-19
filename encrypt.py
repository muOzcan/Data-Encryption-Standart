#!/usr/bin/env python

from f_function import f

def encrypt(düzMetin, altAnahtarlar):

    # DES bir blok şifreleme algoritmasıdır. Bundan dolayı, gelen düzMetin öncelikle bloklara ayrılacaktır
    # Aşağıdaki üç satır düz metni 8 karakterlik (64 bitlik) bloklara ayırıyor ve bloklar listesine ekliyor
    # Örneğin, "üniversi" bir bloktur ve 64-bit uzunluğundadır
    bloklar = []
    for i in range(0, len(düzMetin), 8):
        bloklar.append(düzMetin[i:i+8])


    # Düz metin bloklara ayrıldıktan sonra her bir blok sırasıyla şifrelenecek ve
    # Şifreli bloklar e_list'e eklenecektir
    # Ancak, şifrelemeden önce her bir harfin bu harfe karşılık gelen genişletilmiş ASCII koduna dönüştürülmesi gerekir
    # Bunun için her bir blok öncelikle binary formatına dönüştürülmeli ve ardından _cipher fonksiyonuna gönderilmelidir
    # Örneğin, a harfinin ASCII kodu 0110 0001. Bu dönüşümler için internetten genişletilmiş ASCII tablosu olarak aratabilirsiniz
    # _ascii_to_bin fonksiyonu 8 harflik bir metni 64-bit'lik ikilik tabandaki kodlara dönüştürüyor
    # Böylece, artık şifrelemenin yapılacağı _cipher fonksiyonuna 64-bit'lik bir blok ve 16 tur boyunca kullanılacak alt anahtarlar gönderilebilir
    e_list = []
    for blok in bloklar:
        e_list.append(_cipher(_ascii_to_bin(blok), altAnahtarlar))


    # e_list listesinde toplanan şifreli metinler 1-ASCII sonucu, 2-Hexadecimal sonucu, 3-Binary sonucu şeklinde gönderilebilir
    # Şifreli metni hangi şekilde görmek istiyorsanız onu açık bırakarak diğer seçenekleri pasif duruma getirin
    # Örneğin, şifreli metni ASCII karakterleri şeklinde görmek istiyorsanız birinci seçeneği aktif diğer seçenekleri pasif duruma getirin
    sifreliMetin = ""
    for blok in e_list:
        #sifreliMetin += _bin_to_ascii(blok)    # ASCII sonucu
        #sifreliMetin += hex(int(blok, 2))      # Hex sonucu
        sifreliMetin += blok           # Binary sonucu

    return sifreliMetin


# Her bir bloğu alt anahtarlar ile şifreleyen fonksiyon _cipher fonksiyonudur
# Bu fonksiyon iki parametre alır : 1-64 bitlik blok, 2-alt anahtarlar
def _cipher(bit64, altAnahtarlar):

    # Başlangıç permütasyon tablosu
    # Bu tabloya göre başlangıçta 64-bitlik bloktaki her bir bitin yerleri değiştirilir
    # Örneğin, bit64 bloğunun 58. biti 1. sıraya, 50. biti 2. sıraya, 42. biti 3. sıraya ...
    baslangicPermutasyonTablosu = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final Permütasyon Tablosu
    # Bu tabloya göre şifreleme sonunda elde edilen 64-bitlik bloktaki her bir bitin yerleri değiştirilir
    # Örneğin, 16 tur sonunda elde edilen birlestirilmis bloğunun 40. biti 1. sıraya, 8. biti 2. sıraya, 48.biti 3. sıraya, ...
    finalPermutasyonTablosu = [40,  8, 48, 16, 56, 24, 64, 32,
          39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25]
    

    # Bu kısımda baslangicPermutasyonTablosu kullanılarak ilk ikame işlemi gerçekleştirilir
    # Bu ikame işleminin sonunda blok p'ye dönüşür
    p = ""
    for konum in baslangicPermutasyonTablosu:
        p += bit64[konum-1]


    # İlk ikame işleminin ardından elde edilen yeni p bloğu sol ve sağ olmak üzere iki parçaya ayrılır
    # solParca ilk 32 biti, sagParca sondaki 32 biti ifade eder
    solParca = p[:32]
    sagParca = p[32:]

    
    #for i in range(32):
     #   print(str(i+1) + ".Sag Anahtar: " +str(sagParca[i]))

    # Bu kısımda 16 tur boyunca Feistel yapısı çalıştırılır. Bu yapıyı hatırlamak için önceki dersin slaytına bakabilirsiniz
    # Feistel yapısında her turda sağ parça değişime uğramadan bir sonraki turun sol parçasına atanır
    # Örneğin, 2. turun sol parçası (Sol2) = 1. turun sağ parçası (Sag1)
    # Sol2 = Sağ1 oldu. Peki Sag2 nasıl bulunuyordu? Sağ2 ise f_fonksiyonu(Sağ1, altAnahtar1) XOR Sol1 şeklinde bulunur
    # Böylece, 16 tur boyunca her turda sol ve sağ parça değiştirilmiş olur
    
    for i in range(16):
        temp = sagParca
        sagParca = bin(int(solParca, 2) ^ int(f(sagParca, altAnahtarlar[i]), 2))[2:].zfill(32)
        solParca = temp
      

    # 16 turun sonunda sol ve sağ parçalar birleştirilir ve birlestirilmiş 64-bitlik blok elde edilir
    birlestirilmis = solParca + sagParca
    blokSifreliMetin = ""
    
    # Elde edilen birleştirilmiş 64-bitlik blok finalPermutasyonTablosu kullanılarak son ikame işlemi uygulanır
    for konum in finalPermutasyonTablosu:
        blokSifreliMetin += birlestirilmis[konum-1]

    # Böylece, bir blokluk veri şifrelenmiş olur ve blokSifreliMetin döndürülür
    return blokSifreliMetin






# ASCII metnini binary (bit) dizilerine döndüren fonksiyon
def _ascii_to_bin(metin):
    bitDizisi = ""
    for harf in metin:
        bitDizisi += bin(ord(harf))[2:].zfill(8)

    # Eğer elde edilen bitDizisi 64 bitten daha az sayıda ise geri kalan bitler 0 yapılarak 64'e tamamlanır
    # Örneğin, bitDizisi 56 bit uzunluğunda ise 8 adet 0 biti sona eklenerek 64 bite tamamlanır
    for i in range(64-(len(bitDizisi))):
        bitDizisi += "0"

    return bitDizisi



# Bit dizilerini ASCII metnine dönüştüren fonksiyon
def _bin_to_ascii(bit64):
    metin = ""
    for i in range(0, 64, 8):
        metin += chr(int(bit64[i:i+8], 2))

    return metin

