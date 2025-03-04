import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AdminPage() {
  const [news, setNews] = useState([]);
  const [categories, setCategories] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const navigate = useNavigate();

  // Проверка авторизации
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Вы должны войти как администратор');
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
      .then((data) => setNews(data))
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
        } else {
          alert('Ошибка при добавлении новости');
        }
      })
      .catch((error) => console.error('Ошибка добавления новости:', error));
  };

  return (
    <div>
      <h1>Панель администратора</h1>

      {/* Форма для добавления новостей */}
      <form onSubmit={handleAddNews}>
        <h2>Добавить новость</h2>
        <div>
          <label>Заголовок:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Контент:</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Категория:</label>
          <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} required>
            <option value="">Выберите категорию</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Добавить новость</button>
      </form>

      {/* Список новостей */}
      <h2>Список новостей</h2>
      <ul>
        {news.map((item) => (
          <li key={item.id}>
            <h3>{item.title}</h3>
            <p>{item.content}</p>
            <button onClick={() => alert('Редактирование в разработке')}>Редактировать</button>
            <button onClick={() => alert('Удаление в разработке')}>Удалить</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPage;