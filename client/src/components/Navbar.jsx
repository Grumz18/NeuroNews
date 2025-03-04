import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from '../context/AuthContext';
import { useContext } from "react";


const Navbar = () => {

  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return(
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
                <button className="btn btn-outline-danger" onClick={handleLogout}>
                  Выйти
                </button>
                ) : (
                  <>
                    <Link to="/login" className="btn btn-outline-primary me-2"> Вход </Link>
                    <Link to="/register" className="btn btn-outline-success"> Регистрация </Link>
                  </>
                )}
            </ul>
          </div>
        </div>
      </nav>
  );
}

export default Navbar;