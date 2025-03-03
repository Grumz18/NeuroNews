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
    <div className="row">
      {news.map((item) => (
        <div key={item.id} className="col-md-6 col-lg-4 mb-4">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">{item.title}</h5>
              <p className="card-text">{item.content}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default NewsPage;