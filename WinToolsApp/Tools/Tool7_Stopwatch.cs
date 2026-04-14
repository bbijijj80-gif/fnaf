using System;
using System.Windows.Forms;

namespace Tool7_Stopwatch
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Секундомер", Width = 300, Height = 250, StartPosition = FormStartPosition.CenterScreen };
            
            var label = new Label { Dock = DockStyle.Top, Font = new System.Drawing.Font("Arial", 24), TextAlign = System.Drawing.ContentAlignment.MiddleCenter, Height = 60 };
            var startBtn = new Button { Text = "Старт", Location = new System.Drawing.Point(10, 80), Width = 80, Height = 40 };
            var stopBtn = new Button { Text = "Стоп", Location = new System.Drawing.Point(100, 80), Width = 80, Height = 40 };
            var resetBtn = new Button { Text = "Сброс", Location = new System.Drawing.Point(190, 80), Width = 80, Height = 40 };
            
            var stopwatch = new System.Diagnostics.Stopwatch();
            var timer = new System.Windows.Forms.Timer { Interval = 100 };
            
            timer.Tick += (s, e) =>
            {
                if (stopwatch.IsRunning)
                    label.Text = stopwatch.Elapsed.ToString(@"hh\:mm\:ss\.ff");
            };
            
            startBtn.Click += (s, e) => { if (!stopwatch.IsRunning) { stopwatch.Start(); timer.Start(); } };
            stopBtn.Click += (s, e) => { stopwatch.Stop(); timer.Stop(); };
            resetBtn.Click += (s, e) => { stopwatch.Reset(); timer.Stop(); label.Text = "00:00:00.00"; };
            
            form.Controls.Add(label);
            form.Controls.Add(startBtn);
            form.Controls.Add(stopBtn);
            form.Controls.Add(resetBtn);

            Application.Run(form);
        }
    }
}
