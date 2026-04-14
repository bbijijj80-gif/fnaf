using System;
using System.Windows.Forms;

namespace Tool2_Calculator
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form
            {
                Text = "Калькулятор",
                Width = 300,
                Height = 400,
                StartPosition = FormStartPosition.CenterScreen
            };

            var textBox = new TextBox { Location = new System.Drawing.Point(10, 10), Width = 260, ReadOnly = true };
            form.Controls.Add(textBox);

            string[] buttons = { "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", "=", "+" };
            int x = 10, y = 50;
            foreach (var btnText in buttons)
            {
                var btn = new Button { Text = btnText, Location = new System.Drawing.Point(x, y), Width = 60, Height = 40 };
                btn.Click += (s, e) =>
                {
                    if (btnText == "C") textBox.Clear();
                    else if (btnText == "=")
                    {
                        try { textBox.Text = new System.Data.DataTable().Compute(textBox.Text, null).ToString(); }
                        catch { textBox.Text = "Ошибка"; }
                    }
                    else textBox.Text += btnText;
                };
                form.Controls.Add(btn);
                x += 65;
                if (x > 250) { x = 10; y += 45; }
            }

            Application.Run(form);
        }
    }
}
