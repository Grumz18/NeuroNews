import React from 'react';

function HomePage() {
  return (
    <div className="text-center mt-5">
      <h1 className="display-4">Добро пожаловать в новостной блог!</h1>
      <p className="lead">Здесь вы найдете последние новости и статьи.</p>
      <a href="/news" className="btn btn-primary btn-lg">Перейти к новостям</a>
    </div>
  );
}

export default HomePage;