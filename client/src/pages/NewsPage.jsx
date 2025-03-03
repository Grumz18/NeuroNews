import React, { useEffect, useState } from 'react';

function NewsPage() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    let isMounted = true; // Флаг для предотвращения утечек памяти

    const fetchNews = async () => {
      try {
        const response = await fetch('/api/news');
        if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const data = await response.json();

        if (isMounted) {
          setNews(data); // Обновляем состояние только если компонент смонтирован
        }
      } catch (error) {
        console.error('Ошибка загрузки новостей:', error);
      }
    };

    fetchNews();

    return () => {
      isMounted = false; // Сбрасываем флаг при размонтировании
    };
  }, []);

  return (
    <div>
      <h1>Новости</h1>
      <ul>
        {news.map((item) => (
          <li key={item.id}>
            <h2>{item.title}</h2>
            <p>{item.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default NewsPage;