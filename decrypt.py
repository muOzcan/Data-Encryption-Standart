#!/usr/bin/env python

from f_function import f

def decrypt(cipher, altAnahtarlar):

    # cipher şifreli verisi 64 bitlik bloklara ayrılır
    # Şifreleme için kullanılan alt anahtarların aynısı bu fonksiyona parametre olarak verilmelidir
    # Bu fonksiyonda cipher parametresinin binary olması ZORUNLUDUR
    bloklar = []
    for i in range(0, len(cipher), 64):
        bloklar.append(cipher[i:i+64])


    # Şifreli veri 64-bitlik bloklara ayrıldıktan sonra her bir bloğun şifresi ayrı ayrı çözülür
    # Her bir blok ve alt anahtarlar _plaintext fonksiyonuna parametre olarak verilir
    # Şifresi çözülen blokların düz metin halleri d_list listesine eklenir
    d_list = []
    for blok in bloklar:
        d_list.append(_plaintext(blok, altAnahtarlar))


    # Combine chunks back into a single string
    sifresiCozulmusMetin = ""
    for blok in d_list:
        sifresiCozulmusMetin += _bin_to_ascii(blok)     # ASCII sonucu
        #sifresiCozulmusMetin += hex(int(blok, 2))      # Hex sonucu
        #sifresiCozulmusMetin += blok                   # Binary sonucu

    return sifresiCozulmusMetin


# Her bir şifreli bloğun alt anahtarlar ile şifresini çözen fonksiyon _plaintext fonksiyonudur
# Bu fonksiyon iki parametre alır : 1-64 bitlik şifreli blok, 2-alt anahtarlar
# Şifrelemede kullanılan alt anahtarlar ile aynı anahtarlar olduğunu UNUTMAYINIZ..!!
def _plaintext(bit64, altAnahtarlar):

    # Başlangıç permütasyon tablosu
    # Bu tabloya göre başlangıçta 64-bitlik bloktaki her bir bitin yerleri değiştirilir
    # Örneğin, bit64 bloğunun 58. biti 1. sıraya, 50. biti 2. sıraya, 42. biti 3. sıraya ...
    # Şifrelemede kullanılan ikame tablosuyla aynı tablo olduğuna DİKKAT EDİNİZ...!!!
    baslangicPermutasyonTablosu = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final Permütasyon Tablosu
    # Bu tabloya göre şifre çözme sonunda elde edilen 64-bitlik bloktaki her bir bitin yerleri değiştirilir
    # Örneğin, 16 tur sonunda elde edilen birlestirilmis bloğunun 40. biti 1. sıraya, 8. biti 2. sıraya, 48.biti 3. sıraya, ...
    # Şifrelemede kullanılan ikame tablosuyla aynı tablo olduğuna DİKKAT EDİNİZ...!!!
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
        p+= bit64[konum-1]


    # İlk ikame işleminin ardından elde edilen yeni p bloğu sol ve sağ olmak üzere iki parçaya ayrılır
    # solParca ilk 32 biti, sagParca sondaki 32 biti ifade eder
    solParca = p[:32]
    sagParca = p[32:]

    # Bu kısımda 16 tur boyunca Feistel yapısı çalıştırılır. Bu yapıyı hatırlamak için önceki dersin slaytına bakabilirsiniz
    # Feistel yapısında her turda sol parça değişime uğramadan bir sonraki turun sağ parçasına atanır
    # Örneğin, 2. turun sağ parçası (Sag2) = 1. turun sol parçası (Sol1)
    # Sag2 = Sol1 oldu. Peki Sol2 nasıl bulunuyordu? Sol2 ise f_fonksiyonu(Sol1, altAnahtar1) XOR Sag1 şeklinde bulunur
    # Böylece, 16 tur boyunca her turda sol ve sağ parça değiştirilmiş olur
    for i in range(15, -1, -1):
        temp = solParca
        solParca = bin(int(sagParca, 2) ^ int(f(solParca, altAnahtarlar[i]), 2))[2:].zfill(32)
        sagParca = temp

    # 16 turun sonunda sol ve sağ parçalar birleştirilir ve birlestirilmiş 64-bitlik blok elde edilir
    birlestirilmis = solParca + sagParca
    blokSifresiCozulmusMetin = ""
    for konum in finalPermutasyonTablosu:
        blokSifresiCozulmusMetin += birlestirilmis[konum-1]

    return blokSifresiCozulmusMetin
        



# Binary (bit) dizilerini ASCII metnine döndüren fonksiyon
def _bin_to_ascii(bit64):

    metin = ""
    for i in range(0, 64, 8):
        metin += chr(int(bit64[i:i+8], 2))

    return metin
