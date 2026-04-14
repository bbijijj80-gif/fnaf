using System;
using System.Windows.Forms;

namespace Tool10_WeatherMock
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Погода (демо)", Width = 350, Height = 250, StartPosition = FormStartPosition.CenterScreen };
            
            var cityLabel = new Label { Text = "Город: Москва", Location = new System.Drawing.Point(10, 10), AutoSize = true };
            var tempLabel = new Label { Text = "Температура: +20°C", Location = new System.Drawing.Point(10, 40), Font = new System.Drawing.Font("Arial", 18), AutoSize = true };
            var conditionLabel = new Label { Text = "Ясно", Location = new System.Drawing.Point(10, 80), AutoSize = true };
            var refreshBtn = new Button { Text = "Обновить", Location = new System.Drawing.Point(10, 120), Width = 100, Height = 40 };
            
            var random = new Random();
            refreshBtn.Click += (s, e) =>
            {
                int temp = random.Next(-10, 35);
                string[] conditions = { "Ясно", "Облачно", "Дождь", "Снег", "Туман" };
                tempLabel.Text = $"Температура: {temp}°C";
                conditionLabel.Text = conditions[random.Next(conditions.Length)];
            };
            
            form.Controls.Add(cityLabel);
            form.Controls.Add(tempLabel);
            form.Controls.Add(conditionLabel);
            form.Controls.Add(refreshBtn);
            refreshBtn.PerformClick();

            Application.Run(form);
        }
    }
}
