using System;
using System.Windows.Forms;

namespace Tool9_FileSearch
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Поиск файлов", Width = 500, Height = 400, StartPosition = FormStartPosition.CenterScreen };
            
            var textBox = new TextBox { Location = new System.Drawing.Point(10, 10), Width = 300 };
            var searchBtn = new Button { Text = "Найти", Location = new System.Drawing.Point(320, 8), Width = 80 };
            var listBox = new ListBox { Location = new System.Drawing.Point(10, 50), Width = 460, Height = 300 };
            
            searchBtn.Click += (s, e) =>
            {
                listBox.Items.Clear();
                string pattern = textBox.Text;
                try
                {
                    var files = System.IO.Directory.GetFiles(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), $"*{pattern}*", System.IO.SearchOption.AllDirectories);
                    foreach (var file in files)
                        listBox.Items.Add(file);
                }
                catch (Exception ex) { MessageBox.Show(ex.Message); }
            };
            
            form.Controls.Add(textBox);
            form.Controls.Add(searchBtn);
            form.Controls.Add(listBox);

            Application.Run(form);
        }
    }
}
