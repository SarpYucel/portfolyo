CREATE DATABASE MarketDB;
GO

USE MarketDB;
GO

-- 1. Login Paneli için Kullanıcılar Tablosu
CREATE TABLE Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL,
    Password NVARCHAR(50) NOT NULL
);

-- Sisteme giriş yapabilmek için örnek bir kullanıcı ekleyelim
INSERT INTO Users (Username, Password) VALUES ('admin', '12345');
INSERT INTO Users (Username, Password) VALUES ('sarp', '12345');

-- 2. Müşteri Kayıtları için Ana Tablo
CREATE TABLE Customers (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Phone NVARCHAR(20) NOT NULL,
    Address NVARCHAR(200)
);

-- Test için birkaç örnek müşteri
INSERT INTO Customers (FirstName, LastName, Phone, Address) 
VALUES ('Ahmet', 'Yılmaz', '05551112233', 'İstanbul, Kadıköy');
INSERT INTO Customers (FirstName, LastName, Phone, Address) 
VALUES ('Ayşe', 'Demir', '05324445566', 'Ankara, Çankaya');
GO
