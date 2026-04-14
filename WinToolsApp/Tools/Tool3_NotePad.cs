using System;
using System.Windows.Forms;

namespace Tool3_NotePad
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Блокнот", Width = 500, Height = 400, StartPosition = FormStartPosition.CenterScreen };
            var textBox = new TextBox { Multiline = true, ScrollBars = ScrollBars.Both, Dock = DockStyle.Fill, Font = new System.Drawing.Font("Consolas", 12) };
            form.Controls.Add(textBox);

            var menu = new MenuStrip();
            var fileMenu = new ToolStripMenuItem("Файл");
            var saveItem = new ToolStripMenuItem("Сохранить");
            var openItem = new ToolStripMenuItem("Открыть");
            
            saveItem.Click += (s, e) =>
            {
                using (var dlg = new SaveFileDialog())
                {
                    if (dlg.ShowDialog() == DialogResult.OK)
                        System.IO.File.WriteAllText(dlg.FileName, textBox.Text);
                }
            };
            
            openItem.Click += (s, e) =>
            {
                using (var dlg = new OpenFileDialog())
                {
                    if (dlg.ShowDialog() == DialogResult.OK)
                        textBox.Text = System.IO.File.ReadAllText(dlg.FileName);
                }
            };

            fileMenu.DropDownItems.Add(openItem);
            fileMenu.DropDownItems.Add(saveItem);
            menu.Items.Add(fileMenu);
            form.MainMenuStrip = menu;
            form.Controls.Add(menu);

            Application.Run(form);
        }
    }
}
