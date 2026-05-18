using System;

namespace SatisAnalizi
{
    class Program
    {
        static void Main(string[] args)
        {
            // Kullanıcıdan kaç günlük satış verisi girileceğini alıyoruz
            Console.Write("Kaç günlük satış verisi gireceksiniz: ");
            int gunSayisi = int.Parse(Console.ReadLine());

            // Bu sayı kadar eleman içeren bir double dizi oluşturuyoruz
            double[] satisTutarlari = new double[gunSayisi];

            // Günlük satış tutarlarını kullanıcıdan alarak diziye aktarıyoruz
            for (int i = 0; i < gunSayisi; i++)
            {
                bool gecerliGiris = false;
                while (!gecerliGiris)
                {
                    Console.Write((i + 1) + ". gün satış tutarı: ");
                    double tutar = double.Parse(Console.ReadLine());

                    // Negatif satış tutarına izin vermiyoruz
                    if (tutar < 0)
                    {
                        Console.WriteLine("Hata: Satış tutarı negatif olamaz! Lütfen tekrar giriniz.");
                    }
                    else
                    {
                        satisTutarlari[i] = tutar;
                        gecerliGiris = true;
                    }
                }
            }

            // Hesaplanan tüm sonuçları konsol ekranına yazdırıyoruz
            Console.WriteLine();
            Console.WriteLine("--- Günlük Satışlar ---");
            for (int i = 0; i < gunSayisi; i++)
            {
                Console.WriteLine((i + 1) + ". gün: " + satisTutarlari[i] + " TL");
            }

            Console.WriteLine();
            Console.WriteLine("--- Satış İstatistikleri ---");
            
            double toplamSatis = ToplamSatisHesapla(satisTutarlari);
            Console.WriteLine("Toplam Satış: " + toplamSatis + " TL");

            double ortalamaSatis = OrtalamaSatisHesapla(satisTutarlari);
            Console.WriteLine("Ortalama Satış: " + Math.Round(ortalamaSatis, 2) + " TL");

            double enYuksekSatis = EnYuksekSatisBul(satisTutarlari);
            Console.WriteLine("En Yüksek Satış: " + enYuksekSatis + " TL");

            int enYuksekSatisGunu = EnYuksekSatisGunuBul(satisTutarlari);
            Console.WriteLine("En Yüksek Satışın Yapıldığı Gün: " + enYuksekSatisGunu + ". gün");

            double enDusukSatis = EnDusukSatisBul(satisTutarlari);
            Console.WriteLine("En Düşük Satış: " + enDusukSatis + " TL");

            Console.ReadKey();
        }

        // Günlük satışların toplamını hesaplayan metot
        static double ToplamSatisHesapla(double[] satisTutarlari)
        {
            double toplam = 0;
            for (int i = 0; i < satisTutarlari.Length; i++)
            {
                toplam += satisTutarlari[i];
            }
            return toplam;
        }

        // Günlük satışların ortalamasını hesaplayan metot
        static double OrtalamaSatisHesapla(double[] satisTutarlari)
        {
            double toplam = ToplamSatisHesapla(satisTutarlari);
            double ortalama = toplam / satisTutarlari.Length;
            return ortalama;
        }

        // En yüksek satış tutarını bulan metot
        static double EnYuksekSatisBul(double[] satisTutarlari)
        {
            double enYuksek = satisTutarlari[0];
            for (int i = 1; i < satisTutarlari.Length; i++)
            {
                if (satisTutarlari[i] > enYuksek)
                {
                    enYuksek = satisTutarlari[i];
                }
            }
            return enYuksek;
        }

        // En düşük satış tutarını bulan metot
        static double EnDusukSatisBul(double[] satisTutarlari)
        {
            double enDusuk = satisTutarlari[0];
            for (int i = 1; i < satisTutarlari.Length; i++)
            {
                if (satisTutarlari[i] < enDusuk)
                {
                    enDusuk = satisTutarlari[i];
                }
            }
            return enDusuk;
        }

        // En yüksek satışın yapıldığı günü (1'den başlayarak) bulan metot
        static int EnYuksekSatisGunuBul(double[] satisTutarlari)
        {
            double enYuksek = satisTutarlari[0];
            int enYuksekGun = 1;
            
            for (int i = 1; i < satisTutarlari.Length; i++)
            {
                if (satisTutarlari[i] > enYuksek)
                {
                    enYuksek = satisTutarlari[i];
                    enYuksekGun = i + 1; // 1'den başladığı için i+1
                }
            }
            return enYuksekGun;
        }
    }
}


