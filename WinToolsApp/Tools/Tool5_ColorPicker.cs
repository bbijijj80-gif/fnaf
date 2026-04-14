using System;
using System.Windows.Forms;

namespace Tool5_ColorPicker
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Выбор цвета", Width = 300, Height = 200, StartPosition = FormStartPosition.CenterScreen };
            var panel = new Panel { Dock = DockStyle.Fill };
            form.Controls.Add(panel);

            var btn = new Button { Text = "Выбрать цвет", Dock = DockStyle.Top, Height = 40 };
            btn.Click += (s, e) =>
            {
                using (var dlg = new ColorDialog())
                {
                    if (dlg.ShowDialog() == DialogResult.OK)
                        panel.BackColor = dlg.Color;
                }
            };
            form.Controls.Add(btn);

            Application.Run(form);
        }
    }
}
