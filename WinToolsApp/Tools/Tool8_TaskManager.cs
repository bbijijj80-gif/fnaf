using System;
using System.Windows.Forms;

namespace Tool8_TaskManager
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            var form = new Form { Text = "Диспетчер задач", Width = 500, Height = 400, StartPosition = FormStartPosition.CenterScreen };
            var listBox = new ListBox { Dock = DockStyle.Fill };
            var refreshBtn = new Button { Text = "Обновить", Dock = DockStyle.Bottom, Height = 40 };
            
            refreshBtn.Click += (s, e) =>
            {
                listBox.Items.Clear();
                foreach (System.Diagnostics.Process proc in System.Diagnostics.Process.GetProcesses())
                {
                    try { listBox.Items.Add($"{proc.ProcessName} - PID: {proc.Id}"); }
                    catch { }
                }
            };
            
            listBox.DoubleClick += (s, e) =>
            {
                if (listBox.SelectedItem != null && MessageBox.Show("Завершить процесс?", "Подтверждение", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    var parts = listBox.SelectedItem.ToString().Split(':');
                    if (parts.Length > 1 && int.TryParse(parts[1].Trim(), out int pid))
                    {
                        try { System.Diagnostics.Process.GetProcessById(pid).Kill(); }
                        catch { MessageBox.Show("Не удалось завершить процесс"); }
                    }
                }
            };
            
            form.Controls.Add(listBox);
            form.Controls.Add(refreshBtn);
            refreshBtn.PerformClick();

            Application.Run(form);
        }
    }
}
