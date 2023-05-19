#!/usr/bin/env python

"""
f Fonksiyonu:

- İki parametre alır : Dizi (bit32) biçiminde 32-bit ikili sayı ve dizi (anahtar) biçiminde 48 bit ikili sayı
- Bit32 girdisi üzerinde çeşitli permütasyonlar, genişletmeler ve azaltmalar gerçekleştirir
- Bir dizi biçiminde 32-bit ikili sayı döndürür

"""
def f(bit32, anahtar):

    # 32-bitlik girdiyi 48-bite genişletir ve tam sayıya dönüştürür
    # Genişletme işlemi için _genisletme fonksiyonu içerisinde oluşturulan genişletme tablosu kullanılır
    bit48 = int(_genisletme(bit32), 2)


    # 48-bitlik genişletilmiş bit48 değişkeni ile 48-bit uzunluğundaki alt anahtar XOR işlemine sokulur
    # Elde edilen yeni bit dizisi bit48 değişkenine atanır
    bit48 ^= int(anahtar, 2)
    bit48 = bin(bit48)[2:].zfill(48)
    
    

    # S kutularına göre ikame işlemi gerçekleştirilir
    # Böylece, 48 bitlik veriden 32 bitlik veri elde edilmiş olur
    bit32 = _Sbox(bit48)


    # 32 bitlik veri alarak ikame işlemi gerçekleştirir
    # Bu işlem için ikame permütasyon tablosu kullanılır
    # Örneğin, bit32 dizisinin 16. biti 1.sıraya, 7. biti 2. sıraya, ...
    bit32 = _permute(bit32)
    
    
    
    return bit32


"""
Expansion:

- Bir dizi biçiminde 32 bit ikili sayı alır
- 32 bitlik sayıyı 48 bitlik sayıya dönüştürür ve değiştirir
- Bir dizi biçiminde 48 bit ikili sayı döndürür

"""
def _genisletme(bit32):

    # Genişletme Tablosu
    # Bu tabloda bazı bitler tekrarlanarak 32 bit 48 bite genişletilir
    genisletmeTablosu = [32,  1,  2,  3,  4,  5,
          4,  5,  6,  7,  8,  9,
          8,  9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32,  1]

    # İkame işlemi for döngüsü içerisinde gerçekleştirilir
    # Elde edilen yeni bit dizisi bit48 döndürülür
    bit48 = ""
    for konum in genisletmeTablosu:
        bit48 += bit32[konum-1]

    return bit48



"""
Sbox Substitution:

- Bir dizi biçiminde 48-bitlik ikili sayı alır
- 48-bitlik girdiyi 6 bitlik 8 parçaya böler
- 8 sabit kodlu tablo kullanarak her yığında ikameler gerçekleştirir: 
    > 6 bitlik yığının ilk ve son biti, Sbox'ın satırı için bir koordinat görevi görür 
    > Ortadaki 4 bit, sütun için bir koordinat görevi görür
- Bir dizi biçiminde 32 bit ikili sayı döndürür 

"""
def _Sbox(bit48):

    s = [
         # s1
         [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
          [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
          [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
          [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
         # s2
         [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
          [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
          [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
          [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
         # s3
         [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
          [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
          [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
          [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
         # s4
         [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
          [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
          [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
          [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
         # s5
         [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
          [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
          [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
          [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
         # s6
         [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
          [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
          [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
          [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
         # s7
         [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
          [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
          [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
          [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
         # s8
         [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
          [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
          [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
          [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]
        ]
    
    # 48-bitlik veri 8 adet 6 bitlik parçaya bölünür
    # Her parça bit6_list listesine eklenir
    bit6_list = []
    for i in range(0, 48, 6):
        bit6_list.append(bit48[i:i+6])


    # 6 bitlik bir parçanın ilk ve son biti toplanarak hangi S tablosunun kullanılacağı belirlenir
    # 8 adet S kutusu için işlemler sırasıyla tekrarlanır. 1. 6-bitlik parça S1 kutusunu kullanır, 2. 6-bitlik parça S2 kutusunu kullanır, ...
    # Örneğin, 2. 6-bitlik parça 100101 ise, bu durumda S2 kutusu kullanılacak. Peki S2'nin hangi satırına bakılacak?
    # 6-bitlik parçanın ilk ve son bitinin toplamı yani 100101 için 11 olduğu için sonuncu satırı kullanılacak : S2 kutusunun 4. satırı
    # Ortadaki 4-bit 0010 ise 2'ye eşit olduğundan 3. sutun kullanılacak. Yani 100101 bit dizisi için S2 kutusunun 4. satırının 3. sütunu alınacak
    # S2'nin 4. satırının 3. sütunu 10 olduğu için 100101 yerine 1010 ikame edilecek
    sonuc = ""
    for i in range(8):
        altıBitlikParca = bit6_list[i]
        satır = int(altıBitlikParca[0]+altıBitlikParca[5], 2)
        sütun = int(altıBitlikParca[1:5], 2)

        sonuc += (bin(s[i][satır][sütun])[2:].zfill(4))

    return sonuc



"""
Permute:

- Bir dizi biçiminde 32 bit ikili sayı alır
- Sayı üzerinde basit permütasyon gerçekleştirir
- Bir dizi biçiminde 32 bit ikili sayı döndürür

"""
def _permute(bit32):

    # İkame permütasyon tablosu
    p = [16,  7, 20, 21,
         29, 12, 28, 17,
          1, 15, 23, 26,
          5, 18, 31, 10,
          2,  8, 24, 14,
         32, 27,  3,  9,
         19, 13, 30,  6,
         22, 11,  4, 25]

    # 32-bit üzerinden permütasyon yapar
    sonuc = ""
    for konum in p:
        sonuc += bit32[konum-1]

    return sonuc




