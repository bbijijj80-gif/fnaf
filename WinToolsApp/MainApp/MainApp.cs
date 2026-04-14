using System;
using System.Diagnostics;
using System.Windows.Forms;

namespace MainApp
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "WinTools - Главное меню", Width = 400, Height = 500, StartPosition = FormStartPosition.CenterScreen };
            
            string[] tools = { 
                "1. Информация о системе", 
                "2. Калькулятор", 
                "3. Блокнот", 
                "4. Часы", 
                "5. Выбор цвета",
                "6. Генератор случайных чисел",
                "7. Секундомер",
                "8. Диспетчер задач",
                "9. Поиск файлов",
                "10. Погода (демо)"
            };
            
            string[] exeFiles = { 
                "Tool1_SystemInfo.exe", 
                "Tool2_Calculator.exe", 
                "Tool3_NotePad.exe", 
                "Tool4_Clock.exe", 
                "Tool5_ColorPicker.exe",
                "Tool6_RandomGen.exe",
                "Tool7_Stopwatch.exe",
                "Tool8_TaskManager.exe",
                "Tool9_FileSearch.exe",
                "Tool10_WeatherMock.exe"
            };

            var listBox = new ListBox { Dock = DockStyle.Top, Height = 300 };
            foreach (var tool in tools) listBox.Items.Add(tool);
            
            var launchBtn = new Button { Text = "Запустить", Dock = DockStyle.Bottom, Height = 50, Font = new System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold) };
            launchBtn.Click += (s, e) =>
            {
                if (listBox.SelectedIndex >= 0 && listBox.SelectedIndex < exeFiles.Length)
                {
                    try
                    {
                        string exePath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Tools", exeFiles[listBox.SelectedIndex]);
                        Process.Start(exePath);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка запуска: {ex.Message}\nУбедитесь, что файл {exeFiles[listBox.SelectedIndex]} существует в папке Tools", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                else
                {
                    MessageBox.Show("Выберите инструмент из списка", "Внимание", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            };
            
            var label = new Label { Text = "Выберите инструмент и нажмите Запустить", Dock = DockStyle.Top, Height = 30, TextAlign = System.Drawing.ContentAlignment.MiddleCenter };
            
            form.Controls.Add(launchBtn);
            form.Controls.Add(listBox);
            form.Controls.Add(label);

            Application.Run(form);
        }
    }
}
