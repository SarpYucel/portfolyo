namespace MarketMusteriSistemi
{
    partial class LoginForm
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            lblTitle = new Label();
            txtUsername = new TextBox();
            txtPassword = new TextBox();
            lblUsername = new Label();
            lblPassword = new Label();
            btnLogin = new Button();
            lblWarning = new Label();
            lblCompanyName = new Label();
            panel1 = new Panel();
            lblExit = new Label();
            panel1.SuspendLayout();
            SuspendLayout();
            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font("Segoe UI", 20F, FontStyle.Bold);
            lblTitle.ForeColor = Color.FromArgb(41, 128, 185);
            lblTitle.Location = new Point(340, 50);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(200, 37);
            lblTitle.TabIndex = 1;
            lblTitle.Text = "Kullanıcı Girişi";
            // 
            // txtUsername
            // 
            txtUsername.Font = new Font("Segoe UI", 12F);
            txtUsername.Location = new Point(290, 155);
            txtUsername.Name = "txtUsername";
            txtUsername.Size = new Size(300, 29);
            txtUsername.TabIndex = 3;
            // 
            // txtPassword
            // 
            txtPassword.Font = new Font("Segoe UI", 12F);
            txtPassword.Location = new Point(290, 225);
            txtPassword.Name = "txtPassword";
            txtPassword.PasswordChar = '*';
            txtPassword.Size = new Size(300, 29);
            txtPassword.TabIndex = 5;
            txtPassword.KeyPress += txtPassword_KeyPress;
            // 
            // lblUsername
            // 
            lblUsername.AutoSize = true;
            lblUsername.Font = new Font("Segoe UI", 10F);
            lblUsername.Location = new Point(290, 130);
            lblUsername.Name = "lblUsername";
            lblUsername.Size = new Size(85, 19);
            lblUsername.TabIndex = 2;
            lblUsername.Text = "Kullanıcı Adı:";
            // 
            // lblPassword
            // 
            lblPassword.AutoSize = true;
            lblPassword.Font = new Font("Segoe UI", 10F);
            lblPassword.Location = new Point(290, 200);
            lblPassword.Name = "lblPassword";
            lblPassword.Size = new Size(38, 19);
            lblPassword.TabIndex = 4;
            lblPassword.Text = "Şifre:";
            // 
            // btnLogin
            // 
            btnLogin.BackColor = Color.FromArgb(41, 128, 185);
            btnLogin.FlatStyle = FlatStyle.Flat;
            btnLogin.Font = new Font("Segoe UI", 12F, FontStyle.Bold);
            btnLogin.ForeColor = Color.White;
            btnLogin.Location = new Point(290, 300);
            btnLogin.Name = "btnLogin";
            btnLogin.Size = new Size(300, 45);
            btnLogin.TabIndex = 7;
            btnLogin.Text = "GİRİŞ YAP";
            btnLogin.UseVisualStyleBackColor = false;
            btnLogin.Click += btnLogin_Click;
            // 
            // lblWarning
            // 
            lblWarning.AutoSize = true;
            lblWarning.Font = new Font("Segoe UI", 8F);
            lblWarning.ForeColor = Color.Red;
            lblWarning.Location = new Point(290, 260);
            lblWarning.Name = "lblWarning";
            lblWarning.Size = new Size(183, 13);
            lblWarning.TabIndex = 6;
            lblWarning.Text = "Şifre alanına sadece sayı girilebilir!";
            lblWarning.Visible = false;
            // 
            // lblCompanyName
            // 
            lblCompanyName.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
            lblCompanyName.ForeColor = Color.White;
            lblCompanyName.Location = new Point(12, 160);
            lblCompanyName.Name = "lblCompanyName";
            lblCompanyName.Size = new Size(220, 80);
            lblCompanyName.TabIndex = 0;
            lblCompanyName.Text = "MARKET\nSistemleri";
            lblCompanyName.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // panel1
            // 
            panel1.BackColor = Color.FromArgb(41, 128, 185);
            panel1.Controls.Add(lblCompanyName);
            panel1.Dock = DockStyle.Left;
            panel1.Location = new Point(0, 0);
            panel1.Name = "panel1";
            panel1.Size = new Size(250, 400);
            panel1.TabIndex = 0;
            // 
            // lblExit
            // 
            lblExit.AutoSize = true;
            lblExit.Cursor = Cursors.Hand;
            lblExit.Font = new Font("Segoe UI", 14F, FontStyle.Bold);
            lblExit.ForeColor = Color.Gray;
            lblExit.Location = new Point(620, 10);
            lblExit.Name = "lblExit";
            lblExit.Size = new Size(24, 25);
            lblExit.TabIndex = 8;
            lblExit.Text = "X";
            lblExit.Click += lblExit_Click;
            // 
            // LoginForm
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(650, 400);
            Controls.Add(lblExit);
            Controls.Add(btnLogin);
            Controls.Add(lblWarning);
            Controls.Add(txtPassword);
            Controls.Add(lblPassword);
            Controls.Add(txtUsername);
            Controls.Add(lblUsername);
            Controls.Add(lblTitle);
            Controls.Add(panel1);
            FormBorderStyle = FormBorderStyle.None;
            Name = "LoginForm";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Market Müşteri Sistemi - Giriş";
            panel1.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        private System.Windows.Forms.Label lblTitle;
        private System.Windows.Forms.TextBox txtUsername;
        private System.Windows.Forms.TextBox txtPassword;
        private System.Windows.Forms.Label lblUsername;
        private System.Windows.Forms.Label lblPassword;
        private System.Windows.Forms.Button btnLogin;
        private System.Windows.Forms.Label lblWarning;
        private System.Windows.Forms.Label lblCompanyName;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label lblExit;
    }
}
