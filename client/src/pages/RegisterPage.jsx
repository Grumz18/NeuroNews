import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [gender, setGender] = useState('other');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [captcha, setCaptcha] = useState('');
  const [message, setMessage] = useState(''); // Для вывода сообщений
  const [isError, setIsError] = useState(false); // Для стилизации сообщений
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Проверка подтверждения пароля
    if (password !== confirmPassword) {
      setMessage('Пароли не совпадают');
      setIsError(true);
      return;
    }

    // Проверка капчи
    if (captcha !== '1234') { // Пример сложной капчи
      setMessage('Неверная капча');
      setIsError(true);
      return;
    }

    // Отправка данных на сервер
    fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        password,
        confirm_password: confirmPassword,
        gender,
        date_of_birth: dateOfBirth || null,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          setMessage(data.message);
          setIsError(false);
          setTimeout(() => navigate('/login'), 2000); // Перенаправление на страницу входа
        } else {
          setMessage(data.error || 'Ошибка регистрации');
          setIsError(true);
        }
      })
      .catch((error) => {
        setMessage('Ошибка сети');
        setIsError(true);
      });
  };

  return (
    <div className="container mt-5">
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card shadow">
          <div className="card-body">
            <h2 className="card-title text-center mb-4">Регистрация</h2>
            <p className="text-muted text-center mb-4">
              Пожалуйста, заполните форму для создания учетной записи.
              <br />
              Дополнительные данные помогут нам улучшить рекомендации новостей.
            </p>
            {message && (
              <div
                className={`alert ${
                  isError ? 'alert-danger' : 'alert-success'
                } text-center`}
              >
                {message}
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="email" className="form-label">
                  Email:
                </label>
                <input
                  type="email"
                  id="email"
                  className="form-control"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="password" className="form-label">
                  Пароль:
                </label>
                <input
                  type="password"
                  id="password"
                  className="form-control"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="confirmPassword" className="form-label">
                  Подтвердите пароль:
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  className="form-control"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="gender" className="form-label">
                  Пол:
                </label>
                <select
                  id="gender"
                  className="form-select"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  <option value="male">Мужской</option>
                  <option value="female">Женский</option>
                  <option value="other">Не указан</option>
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="dateOfBirth" className="form-label">
                  Дата рождения (опционально):
                </label>
                <input
                  type="date"
                  id="dateOfBirth"
                  className="form-control"
                  value={dateOfBirth}
                  onChange={(e) => setDateOfBirth(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="captcha" className="form-label">
                  Введите капчу (1234):
                </label>
                <input
                  type="text"
                  id="captcha"
                  className="form-control"
                  value={captcha}
                  onChange={(e) => setCaptcha(e.target.value)}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary w-100">
                Зарегистрироваться
              </button>
            </form>
            <p className="mt-3 text-center">
              Уже есть аккаунт?{' '}
              <Link to="/login" className="text-decoration-none">
                Войти
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
};

export default RegisterPage;