import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AdminPage() {
  const [news, setNews] = useState([]);
  const [categories, setCategories] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [isLoading, setIsLoading] = useState(true); // Индикатор загрузки
  const navigate = useNavigate();

  // Проверка авторизации
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  // Загрузка новостей
  useEffect(() => {
    fetch('http://localhost:5000/admin/news', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
    })
      .then((response) => {
        if (response.ok) return response.json();
        throw new Error('Недостаточно прав');
      })
      .then((data) => {
        setNews(data);
        setIsLoading(false);
      })
      .catch((error) => console.error('Ошибка загрузки новостей:', error));
  }, []);

  // Загрузка категорий
  useEffect(() => {
    fetch('http://localhost:5000/categories')
      .then((response) => response.json())
      .then((data) => setCategories(data))
      .catch((error) => console.error('Ошибка загрузки категорий:', error));
  }, []);

  // Добавление новости
  const handleAddNews = (e) => {
    e.preventDefault();
    fetch('http://localhost:5000/news/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify({ title, content, category_id: categoryId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert('Новость добавлена!');
          setNews([...news, data]);
          setTitle('');
          setContent('');
          setCategoryId('');
        } else {
          alert('Ошибка при добавлении новости');
        }
      })
      .catch((error) => console.error('Ошибка добавления новости:', error));
  };

  return (
    <div className="container mt-4">
      {/* Шапка */}
      <header className="mb-4">
        <h1 className="text-center">Панель администратора</h1>
      </header>

      {/* Форма добавления новостей */}
      <section className="mb-4">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Добавить новость</h2>
          </div>
          <div className="card-body">
            <form onSubmit={handleAddNews}>
              <div className="mb-3">
                <label htmlFor="title" className="form-label">
                  Заголовок:
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="content" className="form-label">
                  Контент:
                </label>
                <textarea
                  className="form-control"
                  id="content"
                  rows="4"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                ></textarea>
              </div>
              <div className="mb-3">
                <label htmlFor="category" className="form-label">
                  Категория:
                </label>
                <select
                  className="form-select"
                  id="category"
                  value={categoryId}
                  onChange={(e) => setCategoryId(e.target.value)}
                  required
                >
                  <option value="">Выберите категорию</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>
              <button type="submit" className="btn btn-primary">
                Добавить новость
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Список новостей */}
      <section>
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Список новостей</h2>
          </div>
          <div className="card-body">
            {isLoading ? (
              <div className="text-center">
                <div className="spinner-border" role="status">
                  <span className="visually-hidden">Загрузка...</span>
                </div>
              </div>
            ) : (
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Заголовок</th>
                    <th>Категория</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {news.map((item) => {
                    const category = categories.find((cat) => cat.id === item.category_id);
                    return (
                      <tr key={item.id}>
                        <td>{item.title}</td>
                        <td>{category ? category.name : 'Без категории'}</td>
                        <td>
                          <button
                            className="btn btn-sm btn-warning me-2"
                            onClick={() => alert('Редактирование в разработке')}
                          >
                            Редактировать
                          </button>
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => alert('Удаление в разработке')}
                          >
                            Удалить
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

export default AdminPage;