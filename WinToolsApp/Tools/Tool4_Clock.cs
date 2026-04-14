using System;
using System.Windows.Forms;

namespace Tool4_Clock
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Часы", Width = 300, Height = 200, StartPosition = FormStartPosition.CenterScreen };
            var label = new Label { Dock = DockStyle.Fill, Font = new System.Drawing.Font("Arial", 36), TextAlign = System.Drawing.ContentAlignment.MiddleCenter };
            form.Controls.Add(label);

            var timer = new System.Windows.Forms.Timer { Interval = 1000 };
            timer.Tick += (s, e) => label.Text = DateTime.Now.ToString("HH:mm:ss");
            timer.Start();

            Application.Run(form);
        }
    }
}
