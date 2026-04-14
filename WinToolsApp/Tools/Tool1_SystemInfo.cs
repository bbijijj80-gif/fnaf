using System;
using System.Diagnostics;
using System.Windows.Forms;

namespace Tool1_SystemInfo
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            string info = $"ОС: {Environment.OSVersion}\n";
            info += $"Процессор: {Environment.ProcessorCount} ядер\n";
            info += $"Память: {GC.GetTotalMemory(false) / 1024 / 1024} MB\n";
            info += $"Время работы: {TimeSpan.FromMilliseconds(Environment.TickCount64)}";
            
            MessageBox.Show(info, "Информация о системе", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
