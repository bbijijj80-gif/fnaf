using System;
using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using HelixToolkit.Wpf;
using Microsoft.Win32;

namespace _3DPrinterModeler
{
    public partial class MainWindow : Window
    {
        private ModelVisual3D? _currentModel;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void AddCube_Click(object sender, RoutedEventArgs e)
        {
            CreatePrimitive("cube");
            StatusText.Text = "Куб добавлен";
        }

        private void AddSphere_Click(object sender, RoutedEventArgs e)
        {
            CreatePrimitive("sphere");
            StatusText.Text = "Сфера добавлена";
        }

        private void AddCylinder_Click(object sender, RoutedEventArgs e)
        {
            CreatePrimitive("cylinder");
            StatusText.Text = "Цилиндр добавлен";
        }

        private void CreatePrimitive(string type)
        {
            if (_currentModel != null)
            {
                MainViewport.Children.Remove(_currentModel);
            }

            MeshGeometry3D mesh = type switch
            {
                "cube" => CreateCubeMesh(1),
                "sphere" => CreateSphereMesh(0.5, 32, 16),
                "cylinder" => CreateCylinderMesh(0.5, 1, 32),
                _ => throw new ArgumentException("Неизвестный тип")
            };

            var model = new ModelVisual3D
            {
                Content = new GeometryModel3D
                {
                    Geometry = mesh,
                    Material = new DiffuseMaterial(new SolidColorBrush(Color.FromRgb(0, 122, 204))),
                    BackMaterial = new DiffuseMaterial(new SolidColorBrush(Color.FromRgb(0, 122, 204)))
                }
            };

            _currentModel = model;
            MainViewport.Children.Add(model);
            MainViewport.ZoomExtents();
        }

        private MeshGeometry3D CreateCubeMesh(double size)
        {
            var mesh = new MeshGeometry3D();
            double s = size / 2;

            // Вершины куба
            mesh.Positions = new Point3DCollection
            {
                new(-s, -s, -s), new(s, -s, -s), new(s, s, -s), new(-s, s, -s), // Задняя грань
                new(-s, -s, s), new(s, -s, s), new(s, s, s), new(-s, s, s),     // Передняя грань
            };

            // Треугольники (индексы вершин)
            int[,] faces = {
                {0, 2, 1}, {0, 3, 2}, // Зад
                {4, 5, 6}, {4, 6, 7}, // Перед
                {0, 1, 5}, {0, 5, 4}, // Низ
                {3, 6, 2}, {3, 7, 6}, // Верх
                {0, 4, 7}, {0, 7, 3}, // Лево
                {1, 2, 6}, {1, 6, 5}  // Право
            };

            for (int i = 0; i < faces.GetLength(0); i++)
            {
                mesh.TriangleIndices.Add(faces[i, 0]);
                mesh.TriangleIndices.Add(faces[i, 1]);
                mesh.TriangleIndices.Add(faces[i, 2]);
            }

            mesh.Normals = GenerateNormals(mesh);
            return mesh;
        }

        private MeshGeometry3D CreateSphereMesh(double radius, int segments, int rings)
        {
            var mesh = new MeshGeometry3D();

            for (int i = 0; i <= rings; i++)
            {
                double phi = Math.PI * i / rings;
                for (int j = 0; j <= segments; j++)
                {
                    double theta = 2 * Math.PI * j / segments;
                    double x = radius * Math.Sin(phi) * Math.Cos(theta);
                    double y = radius * Math.Cos(phi);
                    double z = radius * Math.Sin(phi) * Math.Sin(theta);
                    mesh.Positions.Add(new Point3D(x, y, z));
                }
            }

            for (int i = 0; i < rings; i++)
            {
                for (int j = 0; j < segments; j++)
                {
                    int first = i * (segments + 1) + j;
                    int second = first + segments + 1;
                    mesh.TriangleIndices.Add(first);
                    mesh.TriangleIndices.Add(second);
                    mesh.TriangleIndices.Add(first + 1);
                    mesh.TriangleIndices.Add(second);
                    mesh.TriangleIndices.Add(second + 1);
                    mesh.TriangleIndices.Add(first + 1);
                }
            }

            mesh.Normals = GenerateNormals(mesh);
            return mesh;
        }

        private MeshGeometry3D CreateCylinderMesh(double radius, double height, int segments)
        {
            var mesh = new MeshGeometry3D();
            double h = height / 2;

            // Крышка и дно
            mesh.Positions.Add(new Point3D(0, h, 0)); // Центр верхней крышки
            for (int i = 0; i < segments; i++)
            {
                double angle = 2 * Math.PI * i / segments;
                mesh.Positions.Add(new Point3D(radius * Math.Cos(angle), h, radius * Math.Sin(angle)));
            }

            int bottomCenter = mesh.Positions.Count;
            mesh.Positions.Add(new Point3D(0, -h, 0)); // Центр дна
            for (int i = 0; i < segments; i++)
            {
                double angle = 2 * Math.PI * i / segments;
                mesh.Positions.Add(new Point3D(radius * Math.Cos(angle), -h, radius * Math.Sin(angle)));
            }

            // Верхняя крышка
            for (int i = 0; i < segments - 1; i++)
            {
                mesh.TriangleIndices.Add(0);
                mesh.TriangleIndices.Add(i + 2);
                mesh.TriangleIndices.Add(i + 1);
            }

            // Дно
            for (int i = 0; i < segments - 1; i++)
            {
                mesh.TriangleIndices.Add(bottomCenter);
                mesh.TriangleIndices.Add(bottomCenter + i + 1);
                mesh.TriangleIndices.Add(bottomCenter + i + 2);
            }

            // Боковая поверхность
            int sideStart = 1;
            int bottomStart = bottomCenter + 1;
            for (int i = 0; i < segments - 1; i++)
            {
                mesh.TriangleIndices.Add(sideStart + i);
                mesh.TriangleIndices.Add(sideStart + i + 1);
                mesh.TriangleIndices.Add(bottomStart + i);
                mesh.TriangleIndices.Add(sideStart + i + 1);
                mesh.TriangleIndices.Add(bottomStart + i + 1);
                mesh.TriangleIndices.Add(bottomStart + i);
            }

            mesh.Normals = GenerateNormals(mesh);
            return mesh;
        }

        private Vector3DCollection GenerateNormals(MeshGeometry3D mesh)
        {
            var normals = new Vector3DCollection();
            for (int i = 0; i < mesh.Positions.Count; i++)
            {
                Point3D p = mesh.Positions[i];
                if (p.Length > 0)
                    normals.Add(new Vector3D(p.X, p.Y, p.Z) / p.Length);
                else
                    normals.Add(new Vector3D(0, 1, 0));
            }
            return normals;
        }

        private void DeleteSelected_Click(object sender, RoutedEventArgs e)
        {
            if (_currentModel != null)
            {
                MainViewport.Children.Remove(_currentModel);
                _currentModel = null;
                StatusText.Text = "Объект удален";
            }
        }

        private void ClearAll_Click(object sender, RoutedEventArgs e)
        {
            if (_currentModel != null)
            {
                MainViewport.Children.Remove(_currentModel);
                _currentModel = null;
            }
            StatusText.Text = "Сцена очищена";
        }

        private void ApplyScale_Click(object sender, RoutedEventArgs e)
        {
            if (_currentModel != null && double.TryParse(ScaleBox.Text, out double scale))
            {
                _currentModel.Transform = new ScaleTransform3D(scale, scale, scale);
                StatusText.Text = $"Масштаб применен: {scale}";
            }
        }

        private void ExportSTL_Click(object sender, RoutedEventArgs e)
        {
            ExportModel("stl");
        }

        private void ExportOBJ_Click(object sender, RoutedEventArgs e)
        {
            ExportModel("obj");
        }

        private void Export3MF_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Экспорт в 3MF требует дополнительных библиотек. Используйте STL или OBJ.", 
                          "Информация", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void ExportModel(string format)
        {
            if (_currentModel == null)
            {
                MessageBox.Show("Сначала создайте модель!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var dialog = new SaveFileDialog
            {
                Filter = format.ToUpper() + " files (*." + format + ")|*." + format + "|All files (*.*)|*.*",
                DefaultExt = format,
                FileName = "model3d." + format
            };

            if (dialog.ShowDialog() == true)
            {
                try
                {
                    var geometryModel = _currentModel.Content as GeometryModel3D;
                    if (geometryModel?.Geometry is MeshGeometry3D mesh)
                    {
                        if (format == "stl")
                            SaveAsSTL(mesh, dialog.FileName);
                        else if (format == "obj")
                            SaveAsOBJ(mesh, dialog.FileName);
                        
                        StatusText.Text = $"Экспортировано в {format.ToUpper()}: {Path.GetFileName(dialog.FileName)}";
                        MessageBox.Show($"Модель успешно экспортирована в {dialog.FileName}", 
                                      "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка экспорта: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void SaveAsSTL(MeshGeometry3D mesh, string filename)
        {
            using (var fs = new FileStream(filename, FileMode.Create))
            using (var writer = new BinaryWriter(fs))
            {
                // Заголовок STL (80 байт)
                byte[] header = new byte[80];
                writer.Write(header);
                
                // Количество треугольников
                writer.Write(mesh.TriangleIndices.Count / 3);
                
                // Данные треугольников
                for (int i = 0; i < mesh.TriangleIndices.Count; i += 3)
                {
                    // Нормаль (пока нулевая)
                    writer.Write(0.0f); writer.Write(0.0f); writer.Write(0.0f);
                    
                    // Три вершины
                    for (int j = 0; j < 3; j++)
                    {
                        Point3D p = mesh.Positions[mesh.TriangleIndices[i + j]];
                        writer.Write((float)p.X);
                        writer.Write((float)p.Y);
                        writer.Write((float)p.Z);
                    }
                    
                    // Атрибут (2 байта)
                    writer.Write((ushort)0);
                }
            }
        }

        private void SaveAsOBJ(MeshGeometry3D mesh, string filename)
        {
            using (var writer = new StreamWriter(filename))
            {
                writer.WriteLine("# 3D Printer Modeler OBJ Export");
                writer.WriteLine($"# Вершин: {mesh.Positions.Count}");
                writer.WriteLine($"# Треугольников: {mesh.TriangleIndices.Count / 3}");
                writer.WriteLine();
                
                // Вершины
                foreach (Point3D p in mesh.Positions)
                {
                    writer.WriteLine($"v {p.X:F6} {p.Y:F6} {p.Z:F6}");
                }
                
                writer.WriteLine();
                
                // Грани (треугольники)
                for (int i = 0; i < mesh.TriangleIndices.Count; i += 3)
                {
                    int v1 = mesh.TriangleIndices[i] + 1;
                    int v2 = mesh.TriangleIndices[i + 1] + 1;
                    int v3 = mesh.TriangleIndices[i + 2] + 1;
                    writer.WriteLine($"f {v1} {v2} {v3}");
                }
            }
        }
    }
}
