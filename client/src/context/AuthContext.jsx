import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [role, setRole] = useState(null); // Добавляем состояние для роли

  // Проверка токена при загрузке приложения
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1])); // Декодируем токен
        setIsAuthenticated(true);
        setRole(payload.role); // Устанавливаем роль из токена
      } catch (error) {
        console.error('Ошибка декодирования токена:', error);
      }
    }
  }, []);

  const login = (newRole) => {
    setIsAuthenticated(true);
    setRole(newRole);
  };

  const logout = () => {
    localStorage.removeItem('token'); // Удаляем токен
    setIsAuthenticated(false);
    setRole(null); // Сбрасываем роль
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};