import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);

  if (!isAuthenticated) {
    // Перенаправляем на страницу входа, если пользователь не авторизован
    return <Navigate to="/login" replace />;
  }

  // Рендерим дочерние элементы, если пользователь авторизован
  return children;
};

export default ProtectedRoute;