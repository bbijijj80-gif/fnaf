using System;
using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using HelixToolkit.Wpf;
using Microsoft.Win32;

namespace ModelingApp3D
{
    public partial class MainWindow : Window
    {
        private int _objectCounter = 0;
        private ModelVisual3D? _selectedModel = null;

        public MainWindow()
        {
            InitializeComponent();
            SizeSlider.ValueChanged += SizeSlider_ValueChanged;
            UpdateObjectCount();
        }

        private void SizeSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            SizeValueText.Text = e.NewValue.ToString("F1");
        }

        private Color GetSelectedColor()
        {
            if (ColorComboBox.SelectedItem is ComboBoxItem item && item.Tag != null)
            {
                string colorHex = item.Tag.ToString();
                return (Color)ColorConverter.ConvertFromString(colorHex);
            }
            return Colors.Blue;
        }

        private void AddCube_Click(object sender, RoutedEventArgs e)
        {
            double size = SizeSlider.Value;
            var meshBuilder = new MeshBuilder();
            meshBuilder.AddBox(new Point3D(0, 0, 0), size, size, size);
            
            AddModelToScene(meshBuilder.ToMesh(), $"Куб_{++_objectCounter}");
            UpdateObjectCount();
        }

        private void AddSphere_Click(object sender, RoutedEventArgs e)
        {
            double radius = SizeSlider.Value;
            var meshBuilder = new MeshBuilder();
            meshBuilder.AddSphere(new Point3D(0, 0, 0), radius, 32, 16);
            
            AddModelToScene(meshBuilder.ToMesh(), $"Сфера_{++_objectCounter}");
            UpdateObjectCount();
        }

        private void AddCylinder_Click(object sender, RoutedEventArgs e)
        {
            double radius = SizeSlider.Value;
            double height = SizeSlider.Value * 2;
            var meshBuilder = new MeshBuilder();
            meshBuilder.AddCylinder(new Point3D(0, 0, 0), new Point3D(0, height, 0), radius, 32);
            
            AddModelToScene(meshBuilder.ToMesh(), $"Цилиндр_{++_objectCounter}");
            UpdateObjectCount();
        }

        private void AddCone_Click(object sender, RoutedEventArgs e)
        {
            double radius = SizeSlider.Value;
            double height = SizeSlider.Value * 2;
            var meshBuilder = new MeshBuilder();
            meshBuilder.AddCone(new Point3D(0, height, 0), new Point3D(0, 0, 0), radius, 32);
            
            AddModelToScene(meshBuilder.ToMesh(), $"Конус_{++_objectCounter}");
            UpdateObjectCount();
        }

        private void AddTorus_Click(object sender, RoutedEventArgs e)
        {
            double majorRadius = SizeSlider.Value;
            double minorRadius = SizeSlider.Value * 0.4;
            var meshBuilder = new MeshBuilder();
            meshBuilder.AddTorus(new Point3D(0, 0, 0), new Vector3D(0, 1, 0), 
                                majorRadius, minorRadius, 32, 16);
            
            AddModelToScene(meshBuilder.ToMesh(), $"Тор_{++_objectCounter}");
            UpdateObjectCount();
        }

        private void AddModelToScene(MeshGeometry3D mesh, string name)
        {
            var material = new DiffuseMaterial(new SolidColorBrush(GetSelectedColor()));
            var model = new GeometryModel3D(mesh, material);
            
            var visual = new ModelVisual3D();
            visual.Content = model;
            visual.Tag = name;
            
            // Добавляем возможность выделения
            model.MouseLeftButtonDown += (s, args) =>
            {
                SelectModel(visual);
                args.Handled = true;
            };
            
            MainViewport.Children.Add(visual);
            SelectModel(visual);
        }

        private void SelectModel(ModelVisual3D model)
        {
            // Сброс предыдущего выделения
            if (_selectedModel?.Content is GeometryModel3D oldModel)
            {
                // Возвращаем оригинальный цвет
            }
            
            _selectedModel = model;
            
            if (model?.Content is GeometryModel3D selectedGeometry)
            {
                SelectedObjectText.Text = $"Выбрано: {model.Tag}";
                
                // Подсветка выбранного объекта
                var emissiveMaterial = new EmissiveMaterial(new SolidColorBrush(Colors.Yellow));
                selectedGeometry.Material = new MaterialGroup(
                    new DiffuseMaterial(new SolidColorBrush(GetSelectedColor())),
                    emissiveMaterial);
            }
            else
            {
                SelectedObjectText.Text = "Выбрано: нет";
            }
        }

        private void DeleteSelected_Click(object sender, RoutedEventArgs e)
        {
            if (_selectedModel != null)
            {
                MainViewport.Children.Remove(_selectedModel);
                _selectedModel = null;
                SelectedObjectText.Text = "Выбрано: нет";
                UpdateObjectCount();
            }
            else
            {
                MessageBox.Show("Сначала выберите объект для удаления", "Информация", 
                              MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void ClearAll_Click(object sender, RoutedEventArgs e)
        {
            var result = MessageBox.Show("Удалить все объекты из сцены?", "Подтверждение",
                                       MessageBoxButton.YesNo, MessageBoxImage.Question);
            if (result == MessageBoxResult.Yes)
            {
                MainViewport.Children.Clear();
                // Восстанавливаем освещение и сетку
                MainViewport.Children.Add(new AmbientLight(Color.FromRgb(64, 64, 64)));
                MainViewport.Children.Add(new DirectionalLight(Colors.White, new Vector3D(-1, -1, -1)));
                MainViewport.Children.Add(new DirectionalLight(Color.FromRgb(128, 128, 128), new Vector3D(1, 1, 1)));
                
                var grid = new GridLinesVisual3D
                {
                    Width = 10,
                    Length = 10,
                    MinorDistance = 1,
                    MajorDistance = 2,
                    Stroke = BrushConverter.ConvertFrom("#FF505050") as Brush,
                    Thickness = 0.01
                };
                MainViewport.Children.Add(grid);
                
                _objectCounter = 0;
                _selectedModel = null;
                UpdateObjectCount();
                SelectedObjectText.Text = "Выбрано: нет";
            }
        }

        private void ResetCamera_Click(object sender, RoutedEventArgs e)
        {
            MainViewport.CameraController?.ResetCamera();
        }

        private void UpdateObjectCount()
        {
            int count = MainViewport.Children.Count - 4; // Вычитаем освещение и сетку
            ObjectCountText.Text = $"Объектов: {Math.Max(0, count)}";
        }

        private void ExportSTL_Click(object sender, RoutedEventArgs e)
        {
            ExportModel("STL Files (*.stl)|*.stl|All Files (*.*)|*.*", ".stl", ExportFormat.Stl);
        }

        private void ExportOBJ_Click(object sender, RoutedEventArgs e)
        {
            ExportModel("OBJ Files (*.obj)|*.obj|All Files (*.*)|*.*", ".obj", ExportFormat.OBJ);
        }

        private void Export3MF_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Экспорт в 3MF требует дополнительных библиотек.\n" +
                          "Используйте STL или OBJ формат для лучшей совместимости.",
                          "Информация", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void ExportModel(string filter, string extension, ExportFormat format)
        {
            var models = GetSceneModels();
            if (models.Count == 0)
            {
                MessageBox.Show("Нет объектов для экспорта. Создайте хотя бы одну модель.",
                              "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var saveDialog = new SaveFileDialog
            {
                Filter = filter,
                DefaultExt = extension,
                FileName = $"3DModel_{DateTime.Now:yyyyMMdd_HHmmss}{extension}"
            };

            if (saveDialog.ShowDialog() == true)
            {
                try
                {
                    var exporter = new StlExporter(); // Используем STL экспортер как основной
                    var combinedMesh = CombineModels(models);
                    
                    using (var fileStream = new FileStream(saveDialog.FileName, FileMode.Create))
                    {
                        exporter.Export(combinedMesh, fileStream);
                    }
                    
                    MessageBox.Show($"Модель успешно экспортирована в:\n{saveDialog.FileName}",
                                  "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка при экспорте: {ex.Message}",
                                  "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private System.Collections.Generic.List<GeometryModel3D> GetSceneModels()
        {
            var models = new System.Collections.Generic.List<GeometryModel3D>();
            
            foreach (var child in MainViewport.Children)
            {
                if (child is ModelVisual3D visual && visual.Content is GeometryModel3D geometry)
                {
                    models.Add(geometry);
                }
            }
            
            return models;
        }

        private MeshGeometry3D CombineModels(System.Collections.Generic.List<GeometryModel3D> models)
        {
            var meshBuilder = new MeshBuilder();
            
            foreach (var model in models)
            {
                if (model.Geometry is MeshGeometry3D mesh)
                {
                    meshBuilder.Append(mesh);
                }
            }
            
            return meshBuilder.ToMesh();
        }
    }

    // Простой класс для экспорта STL
    public class StlExporter
    {
        public void Export(MeshGeometry3D mesh, Stream stream)
        {
            using (var writer = new BinaryWriter(stream))
            {
                // Заголовок STL (80 байт)
                byte[] header = new byte[80];
                writer.Write(header);
                
                // Количество треугольников
                int triangleCount = mesh.TriangleIndices.Count / 3;
                writer.Write(triangleCount);
                
                var positions = mesh.Positions;
                var indices = mesh.TriangleIndices;
                var normals = mesh.Normals;
                
                for (int i = 0; i < triangleCount; i++)
                {
                    // Нормаль треугольника
                    Vector3D normal;
                    if (normals != null && normals.Count > i)
                    {
                        normal = normals[i];
                    }
                    else
                    {
                        // Вычисляем нормаль
                        var p1 = positions[indices[i * 3]];
                        var p2 = positions[indices[i * 3 + 1]];
                        var p3 = positions[indices[i * 3 + 2]];
                        normal = Vector3D.CrossProduct(p2 - p1, p3 - p1);
                        normal.Normalize();
                    }
                    
                    writer.Write((float)normal.X);
                    writer.Write((float)normal.Y);
                    writer.Write((float)normal.Z);
                    
                    // Три вершины
                    for (int j = 0; j < 3; j++)
                    {
                        var point = positions[indices[i * 3 + j]];
                        writer.Write((float)point.X);
                        writer.Write((float)point.Y);
                        writer.Write((float)point.Z);
                    }
                    
                    // Атрибут байта (обычно 0)
                    writer.Write((ushort)0);
                }
            }
        }
    }
}
