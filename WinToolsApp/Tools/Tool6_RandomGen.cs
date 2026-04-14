using System;
using System.Windows.Forms;

namespace Tool6_RandomGen
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Генератор случайных чисел", Width = 300, Height = 250, StartPosition = FormStartPosition.CenterScreen };
            
            var label = new Label { Text = "Результат:", Location = new System.Drawing.Point(10, 10), AutoSize = true };
            var resultLabel = new Label { Text = "0", Location = new System.Drawing.Point(10, 40), Font = new System.Drawing.Font("Arial", 24), AutoSize = true };
            var btn = new Button { Text = "Сгенерировать", Location = new System.Drawing.Point(10, 90), Width = 120, Height = 40 };
            
            var random = new Random();
            btn.Click += (s, e) => resultLabel.Text = random.Next(0, 1000).ToString();
            
            form.Controls.Add(label);
            form.Controls.Add(resultLabel);
            form.Controls.Add(btn);

            Application.Run(form);
        }
    }
}
