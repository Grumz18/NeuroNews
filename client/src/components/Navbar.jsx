import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from '../context/AuthContext';
import { useContext } from "react";

const Navbar = () => {
  const { isAuthenticated, role, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link to="/" className="navbar-brand">Новостной блог</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link to="/" className="nav-link">Главная</Link>
            </li>
            <li className="nav-item">
              <Link to="/news" className="nav-link">Новости</Link>
            </li>
            {isAuthenticated ? (
              <>
                {/* Профиль доступен только обычным пользователям */}
                {role === "user" && (
                  <li className="nav-item">
                    <Link to="/profile" className="nav-link">Профиль</Link>
                  </li>
                )}

                {/* Подписки доступны только обычным пользователям */}
                {role === "user" && (
                  <li className="nav-item">
                    <Link to="/subscriptions" className="nav-link">Подписки</Link>
                  </li>
                )}

                {/* Админ-панель доступна только администраторам */}
                {role === "admin" && (
                  <li className="nav-item">
                    <Link to="/admin" className="nav-link">Админ-панель</Link>
                  </li>
                )}

                {/* Кнопка выхода */}
                <li className="nav-item">
                  <button className="btn btn-outline-danger" onClick={handleLogout}>
                    Выйти
                  </button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link to="/login" className="btn btn-outline-primary me-2">Вход</Link>
                </li>
                <li className="nav-item">
                  <Link to="/register" className="btn btn-outline-success">Регистрация</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;