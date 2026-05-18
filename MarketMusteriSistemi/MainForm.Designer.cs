namespace MarketMusteriSistemi
{
    partial class MainForm
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
            panelTop = new Panel();
            lblExit = new Label();
            lblTitle = new Label();
            panelLeft = new Panel();
            btnDelete = new Button();
            btnUpdate = new Button();
            btnAdd = new Button();
            txtAddress = new TextBox();
            lblAddress = new Label();
            txtPhone = new TextBox();
            lblPhone = new Label();
            txtLastName = new TextBox();
            lblLastName = new Label();
            txtFirstName = new TextBox();
            lblFirstName = new Label();
            dgvCustomers = new DataGridView();
            panelTop.SuspendLayout();
            panelLeft.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dgvCustomers).BeginInit();
            SuspendLayout();
            // 
            // panelTop
            // 
            panelTop.BackColor = Color.FromArgb(41, 128, 185);
            panelTop.Controls.Add(lblExit);
            panelTop.Controls.Add(lblTitle);
            panelTop.Dock = DockStyle.Top;
            panelTop.Location = new Point(0, 0);
            panelTop.Name = "panelTop";
            panelTop.Size = new Size(900, 70);
            panelTop.TabIndex = 0;
            // 
            // lblExit
            // 
            lblExit.AutoSize = true;
            lblExit.Cursor = Cursors.Hand;
            lblExit.Font = new Font("Segoe UI", 16F, FontStyle.Bold);
            lblExit.ForeColor = Color.White;
            lblExit.Location = new Point(860, 20);
            lblExit.Name = "lblExit";
            lblExit.Size = new Size(27, 30);
            lblExit.TabIndex = 1;
            lblExit.Text = "X";
            lblExit.Click += lblExit_Click;
            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font("Segoe UI", 20F, FontStyle.Bold);
            lblTitle.ForeColor = Color.White;
            lblTitle.Location = new Point(20, 15);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(380, 37);
            lblTitle.TabIndex = 0;
            lblTitle.Text = " MARKET - Müşteri Yönetimi";
            // 
            // panelLeft
            // 
            panelLeft.BackColor = Color.White;
            panelLeft.Controls.Add(btnDelete);
            panelLeft.Controls.Add(btnUpdate);
            panelLeft.Controls.Add(btnAdd);
            panelLeft.Controls.Add(txtAddress);
            panelLeft.Controls.Add(lblAddress);
            panelLeft.Controls.Add(txtPhone);
            panelLeft.Controls.Add(lblPhone);
            panelLeft.Controls.Add(txtLastName);
            panelLeft.Controls.Add(lblLastName);
            panelLeft.Controls.Add(txtFirstName);
            panelLeft.Controls.Add(lblFirstName);
            panelLeft.Dock = DockStyle.Left;
            panelLeft.Location = new Point(0, 70);
            panelLeft.Name = "panelLeft";
            panelLeft.Size = new Size(300, 530);
            panelLeft.TabIndex = 1;
            // 
            // btnDelete
            // 
            btnDelete.BackColor = Color.FromArgb(231, 76, 60);
            btnDelete.FlatStyle = FlatStyle.Flat;
            btnDelete.Font = new Font("Segoe UI", 11F, FontStyle.Bold);
            btnDelete.ForeColor = Color.White;
            btnDelete.Location = new Point(20, 460);
            btnDelete.Name = "btnDelete";
            btnDelete.Size = new Size(250, 40);
            btnDelete.TabIndex = 10;
            btnDelete.Text = "SİL";
            btnDelete.UseVisualStyleBackColor = false;
            btnDelete.Click += btnDelete_Click;
            // 
            // btnUpdate
            // 
            btnUpdate.BackColor = Color.FromArgb(241, 196, 15);
            btnUpdate.FlatStyle = FlatStyle.Flat;
            btnUpdate.Font = new Font("Segoe UI", 11F, FontStyle.Bold);
            btnUpdate.ForeColor = Color.White;
            btnUpdate.Location = new Point(20, 410);
            btnUpdate.Name = "btnUpdate";
            btnUpdate.Size = new Size(250, 40);
            btnUpdate.TabIndex = 9;
            btnUpdate.Text = "GÜNCELLE";
            btnUpdate.UseVisualStyleBackColor = false;
            btnUpdate.Click += btnUpdate_Click;
            // 
            // btnAdd
            // 
            btnAdd.BackColor = Color.FromArgb(46, 204, 113);
            btnAdd.FlatStyle = FlatStyle.Flat;
            btnAdd.Font = new Font("Segoe UI", 11F, FontStyle.Bold);
            btnAdd.ForeColor = Color.White;
            btnAdd.Location = new Point(20, 360);
            btnAdd.Name = "btnAdd";
            btnAdd.Size = new Size(250, 40);
            btnAdd.TabIndex = 8;
            btnAdd.Text = "EKLE";
            btnAdd.UseVisualStyleBackColor = false;
            btnAdd.Click += btnAdd_Click;
            // 
            // txtAddress
            // 
            txtAddress.Font = new Font("Segoe UI", 12F);
            txtAddress.Location = new Point(20, 255);
            txtAddress.Multiline = true;
            txtAddress.Name = "txtAddress";
            txtAddress.Size = new Size(250, 80);
            txtAddress.TabIndex = 7;
            // 
            // lblAddress
            // 
            lblAddress.AutoSize = true;
            lblAddress.Font = new Font("Segoe UI", 10F);
            lblAddress.Location = new Point(20, 230);
            lblAddress.Name = "lblAddress";
            lblAddress.Size = new Size(47, 19);
            lblAddress.TabIndex = 6;
            lblAddress.Text = "Adres:";
            // 
            // txtPhone
            // 
            txtPhone.Font = new Font("Segoe UI", 12F);
            txtPhone.Location = new Point(20, 185);
            txtPhone.Name = "txtPhone";
            txtPhone.Size = new Size(250, 29);
            txtPhone.TabIndex = 5;
            txtPhone.KeyPress += txtPhone_KeyPress;
            // 
            // lblPhone
            // 
            lblPhone.AutoSize = true;
            lblPhone.Font = new Font("Segoe UI", 10F);
            lblPhone.Location = new Point(20, 160);
            lblPhone.Name = "lblPhone";
            lblPhone.Size = new Size(130, 19);
            lblPhone.TabIndex = 4;
            lblPhone.Text = "Telefon No (Rakam):";
            // 
            // txtLastName
            // 
            txtLastName.Font = new Font("Segoe UI", 12F);
            txtLastName.Location = new Point(20, 115);
            txtLastName.Name = "txtLastName";
            txtLastName.Size = new Size(250, 29);
            txtLastName.TabIndex = 3;
            txtLastName.KeyPress += txtFirstName_KeyPress;
            // 
            // lblLastName
            // 
            lblLastName.AutoSize = true;
            lblLastName.Font = new Font("Segoe UI", 10F);
            lblLastName.Location = new Point(20, 90);
            lblLastName.Name = "lblLastName";
            lblLastName.Size = new Size(49, 19);
            lblLastName.TabIndex = 2;
            lblLastName.Text = "Soyad:";
            // 
            // txtFirstName
            // 
            txtFirstName.Font = new Font("Segoe UI", 12F);
            txtFirstName.Location = new Point(20, 45);
            txtFirstName.Name = "txtFirstName";
            txtFirstName.Size = new Size(250, 29);
            txtFirstName.TabIndex = 1;
            txtFirstName.KeyPress += txtFirstName_KeyPress;
            // 
            // lblFirstName
            // 
            lblFirstName.AutoSize = true;
            lblFirstName.Font = new Font("Segoe UI", 10F);
            lblFirstName.Location = new Point(20, 20);
            lblFirstName.Name = "lblFirstName";
            lblFirstName.Size = new Size(121, 19);
            lblFirstName.TabIndex = 0;
            lblFirstName.Text = "Müşteri Adı (Harf):";
            // 
            // dgvCustomers
            // 
            dgvCustomers.AllowUserToAddRows = false;
            dgvCustomers.AllowUserToDeleteRows = false;
            dgvCustomers.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvCustomers.BackgroundColor = Color.WhiteSmoke;
            dgvCustomers.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgvCustomers.Dock = DockStyle.Fill;
            dgvCustomers.Location = new Point(300, 70);
            dgvCustomers.Name = "dgvCustomers";
            dgvCustomers.ReadOnly = true;
            dgvCustomers.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvCustomers.Size = new Size(600, 530);
            dgvCustomers.TabIndex = 2;
            dgvCustomers.CellClick += dgvCustomers_CellClick;
            // 
            // MainForm
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(900, 600);
            Controls.Add(dgvCustomers);
            Controls.Add(panelLeft);
            Controls.Add(panelTop);
            FormBorderStyle = FormBorderStyle.None;
            Name = "MainForm";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Ana Ekran";
            Load += MainForm_Load;
            panelTop.ResumeLayout(false);
            panelTop.PerformLayout();
            panelLeft.ResumeLayout(false);
            panelLeft.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dgvCustomers).EndInit();
            ResumeLayout(false);
        }

        private System.Windows.Forms.Panel panelTop;
        private System.Windows.Forms.Label lblTitle;
        private System.Windows.Forms.Label lblExit;
        private System.Windows.Forms.Panel panelLeft;
        private System.Windows.Forms.TextBox txtFirstName;
        private System.Windows.Forms.Label lblFirstName;
        private System.Windows.Forms.TextBox txtLastName;
        private System.Windows.Forms.Label lblLastName;
        private System.Windows.Forms.TextBox txtPhone;
        private System.Windows.Forms.Label lblPhone;
        private System.Windows.Forms.TextBox txtAddress;
        private System.Windows.Forms.Label lblAddress;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnUpdate;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.DataGridView dgvCustomers;
    }
}
