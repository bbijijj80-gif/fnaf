using System;
using System.IO;
using System.Windows;
using System.Windows.Media3D;
using HelixToolkit.Wpf;
using Microsoft.Win32;

namespace 3DModelingApp
{
    public partial class MainWindow : Window
    {
        private ModelVisual3DCollection _models;
        
        public MainWindow()
        {
            InitializeComponent();
            _models = MainViewport.Children;
            UpdateModelCount();
        }

        private void AddCube_Click(object sender, RoutedEventArgs e)
        {
            var cubeMesh = new MeshBuilder();
            cubeMesh.AddBox(new Point3D(0, 0, 0), 2, 2, 2);
            
            var model = new GeometryModel3D
            {
                Geometry = cubeMesh.ToMesh(),
                Material = Materials.Blue,
                Transform = new RotateTransform3D(new AxisAngleRotation3D(new Vector3D(1, 0, 0), 45))
            };
            
            var visual = new ModelVisual3D { Content = model };
            _models.Add(visual);
            
            StatusText.Text = "Куб добавлен";
            UpdateModelCount();
        }

        private void AddSphere_Click(object sender, RoutedEventArgs e)
        {
            var sphereMesh = new MeshBuilder();
            sphereMesh.AddSphere(new Point3D(0, 0, 0), 1.5, 30, 30);
            
            var model = new GeometryModel3D
            {
                Geometry = sphereMesh.ToMesh(),
                Material = Materials.Red
            };
            
            var visual = new ModelVisual3D { Content = model };
            _models.Add(visual);
            
            StatusText.Text = "Сфера добавлена";
            UpdateModelCount();
        }

        private void AddCylinder_Click(object sender, RoutedEventArgs e)
        {
            var cylinderMesh = new MeshBuilder();
            cylinderMesh.AddCylinder(new Point3D(0, -1, 0), new Point3D(0, 1, 0), 1, 30);
            
            var model = new GeometryModel3D
            {
                Geometry = cylinderMesh.ToMesh(),
                Material = Materials.Green
            };
            
            var visual = new ModelVisual3D { Content = model };
            _models.Add(visual);
            
            StatusText.Text = "Цилиндр добавлен";
            UpdateModelCount();
        }

        private void ExportSTL_Click(object sender, RoutedEventArgs e)
        {
            if (_models.Count == 0)
            {
                MessageBox.Show("Нет моделей для экспорта!", "Ошибка", 
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var dialog = new SaveFileDialog
            {
                Filter = "STL файлы (*.stl)|*.stl|Все файлы (*.*)|*.*",
                Title = "Экспорт в STL"
            };

            if (dialog.ShowDialog() == true)
            {
                try
                {
                    var exporter = new StlExporter();
                    exporter.Export(MainViewport, dialog.FileName);
                    StatusText.Text = $"STL экспортирован: {Path.GetFileName(dialog.FileName)}";
                    MessageBox.Show($"Файл успешно сохранен:\n{dialog.FileName}", 
                        "Экспорт завершен", MessageBoxButton.OK, MessageBoxImage.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка экспорта: {ex.Message}", "Ошибка", 
                        MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void ExportOBJ_Click(object sender, RoutedEventArgs e)
        {
            if (_models.Count == 0)
            {
                MessageBox.Show("Нет моделей для экспорта!", "Ошибка", 
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var dialog = new SaveFileDialog
            {
                Filter = "OBJ файлы (*.obj)|*.obj|Все файлы (*.*)|*.*",
                Title = "Экспорт в OBJ"
            };

            if (dialog.ShowDialog() == true)
            {
                try
                {
                    var exporter = new ObjExporter();
                    exporter.Export(MainViewport, dialog.FileName);
                    StatusText.Text = $"OBJ экспортирован: {Path.GetFileName(dialog.FileName)}";
                    MessageBox.Show($"Файл успешно сохранен:\n{dialog.FileName}", 
                        "Экспорт завершен", MessageBoxButton.OK, MessageBoxImage.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка экспорта: {ex.Message}", "Ошибка", 
                        MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void ClearScene_Click(object sender, RoutedEventArgs e)
        {
            _models.Clear();
            StatusText.Text = "Сцена очищена";
            UpdateModelCount();
        }

        private void UpdateModelCount()
        {
            ModelCountText.Text = $"Моделей: {_models.Count}";
        }
    }
}
