import math
import random
import threading
import time
from typing import Optional, Tuple

import customtkinter as ctk
from tkinter import messagebox

from database import Database, DatabaseError


# ----------------------------------------------------------------------
# Hesaplama motoru (Mifflin-St Jeor + TDEE + hedefler)
# ----------------------------------------------------------------------


class CalorieEngine:
    """
    BMR/TDEE ve günlük makro hedeflerini hesaplayan sınıf.
    
    Mifflin-St Jeor formülü kullanarak erkek ve kadın için ayrı BMR hesaplar.
    Aktivite seviyesine göre TDEE hesaplar ve hedefe göre kalori ayarlaması yapar.
    """

    ACTIVITY_MULTIPLIERS = {
        "Az Hareketli": 1.2,
        "Orta Hareketli": 1.5,
        "Çok Hareketli": 1.75,
    }

    def __init__(self, age: int, height_cm: float, weight_kg: float, gender: str, activity_level: str, goal: str):
        self.age = age
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.gender = gender
        self.activity_level = activity_level
        self.goal = goal

    def bmr(self) -> float:
        # Mifflin-St Jeor formülü
        # Erkek: 10W + 6.25H − 5A + 5
        # Kadın: 10W + 6.25H − 5A − 161
        base = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age
        if self.gender == "Erkek":
            return base + 5
        else:  # Kadın
            return base - 161

    def tdee(self) -> float:
        bmr = self.bmr()
        multiplier = self.ACTIVITY_MULTIPLIERS.get(self.activity_level, 1.2)
        return bmr * multiplier

    def goal_adjusted_tdee(self) -> float:
        base = self.tdee()
        if self.goal == "Kilo Ver":
            return max(base - 500, 1200)  # güvenlik için alt sınır
        if self.goal == "Kilo Al":
            return base + 500
        return base

    def macro_targets(self) -> Tuple[float, float]:
        """
        Günlük (protein_g, karbonhidrat_g) hedeflerini döndürür.
        - Protein: 1.8 g/kg
        - Karbonhidrat: 3.0 g/kg
        """
        protein = 1.8 * self.weight_kg
        carbs = 3.0 * self.weight_kg
        return protein, carbs

    def daily_water_target(self) -> float:
        """
        Günlük su hedefini ml cinsinden döndürür.
        Genellikle kg başına 30-35 ml veya basitçe 2-3 litre.
        Burada kg başına 33 ml kullanıyoruz (yaklaşık 2-2.5 litre).
        """
        return self.weight_kg * 33.0  # ml cinsinden


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------


class NutritionApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Akıllı Beslenme Planlayıcı")
        self.geometry("960x640")
        self.resizable(False, False)

        # Tema ve renkler
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.bg_color = "#121212"  # deep charcoal
        self.accent_color = "#2ecc71"  # emerald green
        self.fg_color = "#ffffff"  # white

        self.configure(fg_color=self.bg_color)

        # Uygulama durumu
        # ÖNEMLİ: Başka bir bilgisayarda çalıştırırken server adını değiştirin!
        # Bilgisayar adını öğrenmek için: Windows tuşu + R > cmd > hostname
        # Instance adını SSMS'te bağlantı penceresinde görebilirsiniz
        # ÖRNEK: server=r"BILGISAYAR_ADI\SQLEXPRESS" veya server=r"BILGISAYAR_ADI"
        self.db = Database(
            server=r"DESKTOP-JTV1ES3\SQLEXPRESS",  # ⚠️ MUTLAKA DEĞİŞTİRİN: Kendi bilgisayar adınızı ve instance adınızı yazın
            database="NutritionApp",
            trusted_connection=True,
        )

        self.current_user_id: Optional[int] = None

        # Ana frameler
        self.login_frame: Optional[ctk.CTkFrame] = None
        self.register_frame: Optional[ctk.CTkFrame] = None
        self.dashboard_frame: Optional[ctk.CTkFrame] = None

        self.show_login()

    # ------------------------------------------------------------------
    # Frame yardımcıları
    # ------------------------------------------------------------------

    def clear_frames(self) -> None:
        for f in (self.login_frame, self.register_frame, self.dashboard_frame):
            if f is not None:
                f.destroy()

    # ------------------------------------------------------------------
    # Giriş / Kayıt
    # ------------------------------------------------------------------

    def show_login(self) -> None:
        self.clear_frames()
        self.login_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.login_frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(
            self.login_frame,
            text="Hoş Geldiniz",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.fg_color,
        )
        title.pack(pady=(60, 10))

        subtitle = ctk.CTkLabel(
            self.login_frame,
            text="Akıllı beslenme hedeflerini takip etmek için giriş yap",
            font=ctk.CTkFont(size=14),
            text_color="#bbbbbb",
        )
        subtitle.pack(pady=(0, 30))

        form = ctk.CTkFrame(self.login_frame, fg_color="#1e1e1e", corner_radius=16)
        form.pack(pady=10, padx=20)

        username_entry = ctk.CTkEntry(form, placeholder_text="Kullanıcı adı", width=260)
        password_entry = ctk.CTkEntry(form, placeholder_text="Şifre", width=260, show="*")

        username_entry.pack(pady=(20, 10), padx=20)
        password_entry.pack(pady=(0, 20), padx=20)

        message_label = ctk.CTkLabel(form, text="", text_color="#ff6b6b")
        message_label.pack(pady=(0, 10))

        def on_login() -> None:
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                message_label.configure(text="Lütfen hem kullanıcı adı hem de şifre girin.")
                return
            try:
                user_id = self.db.authenticate_user(username, password)
                if user_id is None:
                    message_label.configure(text="Geçersiz kullanıcı adı veya şifre.")
                else:
                    self.current_user_id = user_id
                    self.show_dashboard()
            except DatabaseError as e:
                message_label.configure(text=str(e))

        login_button = ctk.CTkButton(
            form,
            text="Giriş Yap",
            fg_color=self.accent_color,
            hover_color="#27ae60",
            command=on_login,
            width=260,
        )
        login_button.pack(pady=(10, 10))

        switch_label = ctk.CTkLabel(
            form,
            text="Hesabın yok mu?",
            text_color="#aaaaaa",
        )
        switch_label.pack()

        switch_button = ctk.CTkButton(
            form,
            text="Hesap Oluştur",
            fg_color="#333333",
            hover_color="#444444",
            command=self.show_register,
            width=200,
        )
        switch_button.pack(pady=(5, 20))

    def show_register(self) -> None:
        self.clear_frames()
        self.register_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.register_frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(
            self.register_frame,
            text="Hesabını Oluştur",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=self.fg_color,
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self.register_frame,
            text="Beslenme planını kişiselleştirmek için bize kendinden bahset",
            font=ctk.CTkFont(size=14),
            text_color="#bbbbbb",
        )
        subtitle.pack(pady=(0, 20))

        form = ctk.CTkFrame(self.register_frame, fg_color="#1e1e1e", corner_radius=16)
        form.pack(pady=10, padx=20)

        username_entry = ctk.CTkEntry(form, placeholder_text="Kullanıcı adı", width=260)
        password_entry = ctk.CTkEntry(form, placeholder_text="Şifre", width=260, show="*")
        age_entry = ctk.CTkEntry(form, placeholder_text="Yaş (yıl)", width=260)
        height_entry = ctk.CTkEntry(form, placeholder_text="Boy (cm)", width=260)
        weight_entry = ctk.CTkEntry(form, placeholder_text="Kilo (kg)", width=260)

        goal_option = ctk.CTkOptionMenu(form, values=["Kilo Ver", "Kiloyu Koru", "Kilo Al"], width=260)
        goal_option.set("Kilo Ver")

        gender_option = ctk.CTkOptionMenu(form, values=["Erkek", "Kadın"], width=260)
        gender_option.set("Erkek")
        
        activity_option = ctk.CTkOptionMenu(form, values=["Az Hareketli", "Orta Hareketli", "Çok Hareketli"], width=260)
        activity_option.set("Orta Hareketli")

        username_entry.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=2)
        password_entry.grid(row=1, column=0, padx=20, pady=(0, 10), columnspan=2)
        age_entry.grid(row=2, column=0, padx=20, pady=(0, 10))
        height_entry.grid(row=2, column=1, padx=20, pady=(0, 10))
        weight_entry.grid(row=3, column=0, padx=20, pady=(0, 10))
        gender_option.grid(row=3, column=1, padx=20, pady=(0, 10))

        goal_option.grid(row=4, column=0, padx=20, pady=(0, 10))
        activity_option.grid(row=4, column=1, padx=20, pady=(0, 10))

        message_label = ctk.CTkLabel(form, text="", text_color="#ff6b6b")
        message_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        def on_register() -> None:
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            age_text = age_entry.get().strip()
            height_text = height_entry.get().strip()
            weight_text = weight_entry.get().strip()

            if not username or not password:
                message_label.configure(text="Kullanıcı adı ve şifre gereklidir.")
                return

            try:
                age = int(age_text)
                height = float(height_text)
                weight = float(weight_text)
            except ValueError:
                message_label.configure(text="Yaş, boy ve kilo sayısal olmalıdır.")
                return

            if age <= 0 or height <= 0 or weight <= 0:
                message_label.configure(text="Yaş, boy ve kilo pozitif olmalıdır.")
                return

            try:
                success = self.db.register_user(
                    username=username,
                    password=password,
                    age=age,
                    height_cm=height,
                    weight_kg=weight,
                    gender=gender_option.get(),
                    goal=goal_option.get(),
                    activity_level=activity_option.get(),
                )
                if not success:
                    message_label.configure(text="Kullanıcı adı zaten mevcut. Lütfen başka bir tane seç.")
                    return
                message_label.configure(text_color="#2ecc71", text="Hesap oluşturuldu! Artık giriş yapabilirsin.")
                self.after(1000, self.show_login)
            except DatabaseError as e:
                message_label.configure(text=str(e), text_color="#ff6b6b")

        register_button = ctk.CTkButton(
            form,
            text="Hesap Oluştur",
            fg_color=self.accent_color,
            hover_color="#27ae60",
            command=on_register,
            width=260,
        )
        register_button.grid(row=6, column=0, columnspan=2, pady=(10, 20))

        back_button = ctk.CTkButton(
            self.register_frame,
            text="Girişe Dön",
            fg_color="#333333",
            hover_color="#444444",
            command=self.show_login,
            width=180,
        )
        back_button.pack(pady=(10, 20))

    # ------------------------------------------------------------------
    # Kontrol Paneli
    # ------------------------------------------------------------------

    def show_dashboard(self) -> None:
        if self.current_user_id is None:
            self.show_login()
            return

        self.clear_frames()
        self.dashboard_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.dashboard_frame.pack(expand=True, fill="both")

        # Üst çubuk
        top_bar = ctk.CTkFrame(self.dashboard_frame, fg_color="#1a1a1a", height=60)
        top_bar.pack(fill="x", side="top")

        profile = self.db.get_user_profile(self.current_user_id)
        username = profile["Username"] if profile else "Kullanıcı"
        
        from datetime import datetime
        today_str = datetime.now().strftime("%d %B %Y")

        title = ctk.CTkLabel(
            top_bar,
            text=f"Kontrol Paneli · {username} · {today_str}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.fg_color,
        )
        title.pack(side="left", padx=20, pady=10)

        logout_button = ctk.CTkButton(
            top_bar,
            text="Çıkış Yap",
            fg_color="#333333",
            hover_color="#444444",
            command=self._logout,
            width=80,
        )
        logout_button.pack(side="right", padx=20, pady=10)

        # Ana içerik bölümü: sol = ilerleme, sağ = öneri
        content = ctk.CTkFrame(self.dashboard_frame, fg_color=self.bg_color)
        content.pack(expand=True, fill="both", padx=20, pady=20)

        # Sol panel için scrollable container
        left_container = ctk.CTkFrame(content, fg_color=self.bg_color)
        left_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        left = ctk.CTkScrollableFrame(left_container, fg_color="#1e1e1e", corner_radius=16)
        left.pack(fill="both", expand=True)
        
        right = ctk.CTkFrame(content, fg_color="#1e1e1e", corner_radius=16)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Sol: İlerleme çubukları
        progress_title = ctk.CTkFrame(left, fg_color="#1e1e1e")
        progress_title.pack(fill="x", padx=20, pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            progress_title,
            text="Bugünkü Makro İlerlemen",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.fg_color,
        )
        title_label.pack(side="left", anchor="w")

        self.calorie_bar, self.calorie_label, self.calorie_value_label = self._create_progress_row(left, "Kalori")
        self.protein_bar, self.protein_label, self.protein_value_label = self._create_progress_row(left, "Protein (g)")
        self.carbs_bar, self.carbs_label, self.carbs_value_label = self._create_progress_row(left, "Karbonhidrat (g)")

        self.progress_subtitle = ctk.CTkLabel(
            left,
            text="Kişiselleştirilmiş günlük hedeflerine göre",
            text_color="#aaaaaa",
        )
        self.progress_subtitle.pack(padx=20, pady=(10, 10), anchor="w")
        
        # İlerlemeyi sıfırla butonu
        reset_button = ctk.CTkButton(
            left,
            text="İlerlemeyi Sıfırla",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self._reset_today_progress,
            width=180,
            font=ctk.CTkFont(size=12),
        )
        reset_button.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Su takibi bölümü
        water_title = ctk.CTkLabel(
            left,
            text="Su İçme Takibi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.fg_color,
        )
        water_title.pack(padx=20, pady=(10, 10), anchor="w")
        
        # Su progress bar ve kontroller
        water_frame = ctk.CTkFrame(left, fg_color="#1e1e1e")
        water_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Su bilgisi satırı
        water_info_row = ctk.CTkFrame(water_frame, fg_color="#1e1e1e")
        water_info_row.pack(fill="x", padx=10, pady=(10, 5))
        
        water_value_label = ctk.CTkLabel(
            water_info_row,
            text="0 ml / 0 ml",
            text_color="#dddddd",
            font=ctk.CTkFont(size=13),
        )
        water_value_label.pack(side="left", anchor="w")
        
        water_percent_label = ctk.CTkLabel(
            water_info_row,
            text="0%",
            text_color="#3498db",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        water_percent_label.pack(side="right", anchor="e")
        
        # Su progress bar (mavi)
        water_bar = ctk.CTkProgressBar(water_frame, progress_color="#3498db")
        water_bar.set(0.0)
        water_bar.pack(fill="x", padx=10, pady=(5, 10))
        
        # Su kontrol butonları
        water_controls = ctk.CTkFrame(water_frame, fg_color="#1e1e1e")
        water_controls.pack(fill="x", padx=10, pady=(0, 10))
        
        minus_button = ctk.CTkButton(
            water_controls,
            text="- 200 ml",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda: self._adjust_water(-200),
            width=100,
            font=ctk.CTkFont(size=12),
        )
        minus_button.pack(side="left", padx=(0, 10))
        
        plus_button = ctk.CTkButton(
            water_controls,
            text="+ 200 ml",
            fg_color="#3498db",
            hover_color="#2980b9",
            command=lambda: self._adjust_water(200),
            width=100,
            font=ctk.CTkFont(size=12),
        )
        plus_button.pack(side="left")
        
        # Referansları sakla
        self.water_bar = water_bar
        self.water_value_label = water_value_label
        self.water_percent_label = water_percent_label
        
        # Bugünkü öğün geçmişi
        meals_title = ctk.CTkLabel(
            left,
            text="Bugünkü Öğünler",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.fg_color,
        )
        meals_title.pack(padx=20, pady=(10, 10), anchor="w")
        
        # Öğün listesi için normal frame (sol panel zaten scrollable)
        meals_frame = ctk.CTkFrame(left, fg_color="#1e1e1e")
        meals_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.meals_container = meals_frame  # Store reference for updates

        # Sağ: Öğün önerisi kartı
        ctk.CTkLabel(
            right,
            text="Akıllı Öğün Önerisi",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.fg_color,
        ).pack(pady=(20, 10), padx=20, anchor="w")

        self.meal_name_label = ctk.CTkLabel(
            right,
            text="Başlamak için \"Öğün Öner\" butonuna tıkla",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.accent_color,
            wraplength=360,
            justify="left",
        )
        self.meal_name_label.pack(pady=(10, 5), padx=20, anchor="w")

        self.meal_details_label = ctk.CTkLabel(
            right,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#dddddd",
            wraplength=360,
            justify="left",
        )
        self.meal_details_label.pack(pady=(0, 10), padx=20, anchor="w")

        self.meal_status_label = ctk.CTkLabel(
            right,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            wraplength=360,
            justify="left",
        )
        self.meal_status_label.pack(pady=(0, 10), padx=20, anchor="w")

        button_row = ctk.CTkFrame(right, fg_color="#1e1e1e")
        button_row.pack(pady=(10, 20), padx=20, anchor="w")

        suggest_button = ctk.CTkButton(
            button_row,
            text="Öğün Öner",
            fg_color=self.accent_color,
            hover_color="#27ae60",
            command=self._suggest_meal,
            width=200,
        )
        suggest_button.grid(row=0, column=0, padx=(0, 10))

        self.log_button = ctk.CTkButton(
            button_row,
            text="Bu Öğünü Kaydet",
            fg_color="#333333",
            hover_color="#444444",
            command=self._log_suggested_meal,
            width=200,
            state="disabled",
        )
        self.log_button.grid(row=0, column=1)

        # Son öneriyi sakla
        self._last_suggested_meal = None  # (meal_id, grams, calories, protein, carbs)

        # İlk ilerleme yüklemesi, su takibini güncelle ve öğün geçmişini göster
        self._update_progress(animated=False)
        self._update_water_progress()
        self._refresh_meal_history()

    def _logout(self) -> None:
        self.current_user_id = None
        self.show_login()

    def _create_progress_row(self, parent: ctk.CTkFrame, label: str) -> Tuple[ctk.CTkProgressBar, ctk.CTkLabel, ctk.CTkLabel]:
        row = ctk.CTkFrame(parent, fg_color="#1e1e1e")
        row.pack(fill="x", padx=20, pady=10)
        
        # Üst satır: Label ve değerler
        top_row = ctk.CTkFrame(row, fg_color="#1e1e1e")
        top_row.pack(fill="x")
        ctk.CTkLabel(top_row, text=label, text_color=self.fg_color, font=ctk.CTkFont(size=13)).pack(side="left", anchor="w")
        
        # Değer ve yüzde label'ı (sağda)
        value_label = ctk.CTkLabel(
            top_row, 
            text="0 / 0 (0%)", 
            text_color="#aaaaaa", 
            font=ctk.CTkFont(size=11)
        )
        value_label.pack(side="right", anchor="e", padx=(0, 5))
        
        percent_label = ctk.CTkLabel(
            top_row, 
            text="0%", 
            text_color=self.accent_color, 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        percent_label.pack(side="right", anchor="e")
        
        bar = ctk.CTkProgressBar(row, progress_color=self.accent_color)
        bar.set(0.0)
        bar.pack(fill="x", pady=(5, 0))
        return bar, percent_label, value_label

    # ------------------------------------------------------------------
    # İlerleme ve öneri mantığı
    # ------------------------------------------------------------------

    def _build_engine(self) -> Optional[CalorieEngine]:
        if self.current_user_id is None:
            return None
        profile = self.db.get_user_profile(self.current_user_id)
        if not profile:
            return None
        return CalorieEngine(
            age=profile["Age"],
            height_cm=profile["Height_cm"],
            weight_kg=profile["Weight_kg"],
            gender=profile["Gender"],
            activity_level=profile["ActivityLevel"],
            goal=profile["Goal"],
        )

    def _update_progress(self, animated: bool = True) -> None:
        if self.current_user_id is None:
            return

        engine = self._build_engine()
        if not engine:
            return

        total_calories_target = engine.goal_adjusted_tdee()
        protein_target, carbs_target = engine.macro_targets()

        today_calories, today_protein, today_carbs = self.db.get_daily_totals(self.current_user_id)

        cal_ratio = min(today_calories / total_calories_target, 1.0) if total_calories_target > 0 else 0.0
        prot_ratio = min(today_protein / protein_target, 1.0) if protein_target > 0 else 0.0
        carb_ratio = min(today_carbs / carbs_target, 1.0) if carbs_target > 0 else 0.0

        subtitle = (
            f"Günlük hedef · {int(total_calories_target)} kcal · "
            f"{int(protein_target)} g protein · {int(carbs_target)} g karbonhidrat"
        )
        self.progress_subtitle.configure(text=subtitle)

        # Yüzde ve değerleri güncelle
        self.calorie_label.configure(text=f"{cal_ratio * 100:.1f}%")
        self.protein_label.configure(text=f"{prot_ratio * 100:.1f}%")
        self.carbs_label.configure(text=f"{carb_ratio * 100:.1f}%")
        
        # Mevcut / hedef değerlerini göster
        self.calorie_value_label.configure(text=f"{int(today_calories)} / {int(total_calories_target)} kcal")
        self.protein_value_label.configure(text=f"{today_protein:.1f} / {protein_target:.1f} g")
        self.carbs_value_label.configure(text=f"{today_carbs:.1f} / {carbs_target:.1f} g")
        
        if not animated:
            self.calorie_bar.set(cal_ratio)
            self.protein_bar.set(prot_ratio)
            self.carbs_bar.set(carb_ratio)
            return

        # UI'ı bloke etmemek için arka plan thread'i kullanarak basit animasyon
        def animate_bar(bar: ctk.CTkProgressBar, percent_label: ctk.CTkLabel, value_label: ctk.CTkLabel, 
                       current: float, target_val: float, target_label: str, target: float) -> None:
            start = bar.get()
            steps = 20
            for i in range(1, steps + 1):
                value = start + (target - start) * (i / steps)
                current_val = current + (target_val - current) * (i / steps)
                self.after(0, bar.set, value)
                self.after(0, percent_label.configure, {"text": f"{value * 100:.1f}%"})
                if target_label == "kcal":
                    self.after(0, value_label.configure, {"text": f"{int(current_val)} / {int(target_val)} {target_label}"})
                else:
                    self.after(0, value_label.configure, {"text": f"{current_val:.1f} / {target_val:.1f} {target_label}"})
                time.sleep(0.02)

        threading.Thread(
            target=animate_bar, 
            args=(self.calorie_bar, self.calorie_label, self.calorie_value_label, 
                  today_calories, total_calories_target, "kcal", cal_ratio), 
            daemon=True
        ).start()
        threading.Thread(
            target=animate_bar, 
            args=(self.protein_bar, self.protein_label, self.protein_value_label, 
                  today_protein, protein_target, "g", prot_ratio), 
            daemon=True
        ).start()
        threading.Thread(
            target=animate_bar, 
            args=(self.carbs_bar, self.carbs_label, self.carbs_value_label, 
                  today_carbs, carbs_target, "g", carb_ratio), 
            daemon=True
        ).start()

    def _goal_to_category(self, goal: str) -> str:
        if goal == "Kilo Ver":
            return "WeightLoss"
        if goal == "Kilo Al":
            return "Bulk"
        return "Balanced"

    def _suggest_meal(self) -> None:
        if self.current_user_id is None:
            return

        engine = self._build_engine()
        if not engine:
            self.meal_status_label.configure(text="Öneri için kullanıcı profili yüklenemedi.")
            return

        daily_target = engine.goal_adjusted_tdee()
        one_third_target = daily_target / 3.0

        profile = self.db.get_user_profile(self.current_user_id)
        category = self._goal_to_category(profile["Goal"])

        meals = self.db.get_meals_by_category(category)
        if not meals:
            self.meal_status_label.configure(text="Hedef kategoriniz için öğün bulunamadı.")
            return

        # Rastgele bir öğün seç (çeşitlilik için)
        # Önce makul kalori aralığında olanları filtrele (aşırı gram değerlerinden kaçınmak için)
        reasonable_meals = [
            m for m in meals 
            if 100 <= m["Calories_per_100g"] <= 400  # Makul kalori aralığı
        ]
        
        # Eğer makul öğün yoksa tüm öğünlerden seç
        if not reasonable_meals:
            reasonable_meals = meals
        
        # Rastgele bir öğün seç
        best_meal = random.choice(reasonable_meals)

        cal_per_100 = best_meal["Calories_per_100g"]
        if cal_per_100 <= 0:
            grams = 0
        else:
            grams = one_third_target / cal_per_100 * 100.0

        grams = max(50.0, grams)  # makul bir minimum porsiyon zorunluluğu

        calories = cal_per_100 * grams / 100.0
        protein = best_meal["Protein_per_100g"] * grams / 100.0
        carbs = best_meal["Carbs_per_100g"] * grams / 100.0

        self.meal_name_label.configure(
            text=f"{best_meal['MealName']}",
        )

        self.meal_details_label.configure(
            text=(
                f"Önerilen porsiyon: {grams:.0f} g\n"
                f"Yaklaşık {calories:.0f} kcal · {protein:.1f} g protein · {carbs:.1f} g karbonhidrat\n"
                f"(≈ günlük kalori hedefinin 1/3'ü)"
            )
        )

        self.meal_status_label.configure(
            text="Bugünkü alımına eklemek için \"Bu Öğünü Kaydet\" butonuna tıkla.",
            text_color="#aaaaaa",
        )

        self._last_suggested_meal = (best_meal["ID"], grams, calories, protein, carbs)
        self.log_button.configure(state="normal", fg_color=self.accent_color, hover_color="#27ae60")

    def _log_suggested_meal(self) -> None:
        if self.current_user_id is None or not self._last_suggested_meal:
            return
        meal_id, grams, _, _, _ = self._last_suggested_meal
        try:
            self.db.log_meal(self.current_user_id, meal_id, grams)
            self.meal_status_label.configure(
                text="Öğün bugün için kaydedildi! İlerleme çubukları güncellendi.",
                text_color=self.accent_color,
            )
            self.log_button.configure(state="disabled", fg_color="#333333")
            self._update_progress(animated=True)
            self._refresh_meal_history()  # Öğün geçmişini yenile
        except DatabaseError as e:
            self.meal_status_label.configure(text=str(e), text_color="#ff6b6b")

    def _reset_today_progress(self) -> None:
        """Bugünkü tüm kayıtları siler ve progress bar'ları sıfırlar."""
        if self.current_user_id is None:
            return
        
        from tkinter import messagebox
        
        # Onay mesajı
        result = messagebox.askyesno(
            "İlerlemeyi Sıfırla",
            "Bugünkü tüm öğün kayıtlarını silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz.",
            icon="warning"
        )
        
        if not result:
            return
        
        try:
            self.db.clear_today_logs(self.current_user_id)
            # Progress bar'ları güncelle
            self._update_progress(animated=True)
            # Önerilen öğünü de temizle
            self._last_suggested_meal = None
            self.log_button.configure(state="disabled", fg_color="#333333")
            self._refresh_meal_history()  # Öğün geçmişini temizle
            self.meal_status_label.configure(
                text="Bugünkü ilerleme sıfırlandı. Yeni öğünler ekleyebilirsiniz.",
                text_color=self.accent_color,
            )
        except DatabaseError as e:
            messagebox.showerror("Hata", f"İlerleme sıfırlanamadı: {e}")

    def _refresh_meal_history(self) -> None:
        """Bugünkü öğün geçmişini gösterir."""
        if self.current_user_id is None or not hasattr(self, 'meals_container'):
            return
        
        # Mevcut içeriği temizle
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        try:
            meals = self.db.get_today_meals(self.current_user_id)
            
            if not meals:
                empty_label = ctk.CTkLabel(
                    self.meals_container,
                    text="Henüz bugün için öğün eklenmedi.",
                    text_color="#888888",
                    font=ctk.CTkFont(size=12),
                )
                empty_label.pack(pady=10)
                return
            
            for meal in meals:
                meal_frame = ctk.CTkFrame(self.meals_container, fg_color="#2a2a2a", corner_radius=8)
                meal_frame.pack(fill="x", pady=5, padx=0)
                
                # Sol taraf: Öğün bilgileri
                info_frame = ctk.CTkFrame(meal_frame, fg_color="#2a2a2a")
                info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
                
                meal_name = ctk.CTkLabel(
                    info_frame,
                    text=meal["MealName"],
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=self.fg_color,
                )
                meal_name.pack(anchor="w")
                
                meal_details = ctk.CTkLabel(
                    info_frame,
                    text=f"{meal['Grams']:.0f} g · {meal['Calories']:.0f} kcal · {meal['Protein']:.1f}g protein · {meal['Carbs']:.1f}g karbonhidrat",
                    font=ctk.CTkFont(size=11),
                    text_color="#aaaaaa",
                )
                meal_details.pack(anchor="w", pady=(2, 0))
                
                # Sağ taraf: Sil butonu
                delete_button = ctk.CTkButton(
                    meal_frame,
                    text="✕",
                    fg_color="#e74c3c",
                    hover_color="#c0392b",
                    command=lambda log_id=meal["ID"]: self._delete_meal_log(log_id),
                    width=30,
                    height=30,
                    font=ctk.CTkFont(size=14, weight="bold"),
                )
                delete_button.pack(side="right", padx=10, pady=8)
        
        except DatabaseError as e:
            error_label = ctk.CTkLabel(
                self.meals_container,
                text=f"Hata: {str(e)}",
                text_color="#ff6b6b",
                font=ctk.CTkFont(size=11),
            )
            error_label.pack(pady=10)

    def _delete_meal_log(self, log_id: int) -> None:
        """Bir öğün kaydını siler."""
        if self.current_user_id is None:
            return
        
        from tkinter import messagebox
        
        result = messagebox.askyesno(
            "Öğünü Sil",
            "Bu öğünü silmek istediğinize emin misiniz?",
            icon="question"
        )
        
        if not result:
            return
        
        try:
            self.db.delete_meal_log(log_id)
            self._update_progress(animated=True)
            self._refresh_meal_history()
            self.meal_status_label.configure(
                text="Öğün silindi. İlerleme çubukları güncellendi.",
                text_color=self.accent_color,
            )
        except DatabaseError as e:
            messagebox.showerror("Hata", f"Öğün silinemedi: {e}")

    def _update_water_progress(self) -> None:
        """Su takibi progress bar'ını günceller."""
        if self.current_user_id is None or not hasattr(self, 'water_bar'):
            return
        
        try:
            profile = self.db.get_user_profile(self.current_user_id)
            if not profile:
                return
            
            # Su hedefini hesapla
            engine = CalorieEngine(
                profile["Age"],
                profile["Height_cm"],
                profile["Weight_kg"],
                profile["Gender"],
                profile["ActivityLevel"],
                profile["Goal"],
            )
            target_ml = engine.daily_water_target()
            
            # Bugünkü su miktarını al
            current_ml = self.db.get_today_water(self.current_user_id)
            
            # Progress bar'ı güncelle
            progress = min(1.0, current_ml / target_ml) if target_ml > 0 else 0.0
            self.water_bar.set(progress)
            
            # Label'ları güncelle
            self.water_value_label.configure(text=f"{current_ml:.0f} ml / {target_ml:.0f} ml")
            percent = (current_ml / target_ml * 100) if target_ml > 0 else 0.0
            self.water_percent_label.configure(text=f"{percent:.0f}%")
            
        except DatabaseError as e:
            # Hata durumunda sessizce devam et
            pass

    def _adjust_water(self, amount_ml: float) -> None:
        """Su miktarını artırır veya azaltır."""
        if self.current_user_id is None:
            return
        
        try:
            if amount_ml > 0:
                self.db.add_water(self.current_user_id, amount_ml)
            else:
                self.db.subtract_water(self.current_user_id, abs(amount_ml))
            
            self._update_water_progress()
        except DatabaseError as e:
            messagebox.showerror("Hata", f"Su miktarı güncellenemedi: {e}")


if __name__ == "__main__":
    app = NutritionApp()
    app.mainloop()

