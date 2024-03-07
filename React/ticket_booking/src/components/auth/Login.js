import axios from "axios";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { setUser } from "../../store/authSlice";
import Navbar from "../Navbar";
import { useNavigate } from "react-router-dom";

function Login() {
    var [username, setUsername] = useState('');
    var [password, setPassword] = useState('');
    var [errorMessage, setErrorMessage] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    function attemptLogin() {
        axios.post('http://127.0.0.1:8000/api/login/', {
            username: username,
            password: password
        }).then(response => {
            setErrorMessage('');
            var user = {
                username: username,
                token: response.data.token
            };
            dispatch(setUser(user));
            navigate("/");
        }).catch(error => {
            if (error.response.data.non_field_errors) {
                setErrorMessage(error.response.data.non_field_errors[0]);
            } else {
                setErrorMessage('Failed to login user. Please contact admin');
            }
        });
    }

    return (
        <div>
            <Navbar />
            <div className="container">
                <div className="row">
                    <div className="col-8 offset-2">
                        <h1>Login</h1>
                        {errorMessage ? <div className="alert alert-danger">{errorMessage}</div> : ''}
                        <div className="form-group">
                            <label>Username:</label>
                            <input
                                type="text"
                                className="form-control"
                                value={username}
                                onInput={(event) => setUsername(event.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Password:</label>
                            <input
                                type="password"
                                className="form-control"
                                value={password}
                                onInput={(event) => setPassword(event.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <button className="btn btn-primary float-right" onClick={attemptLogin}>Login</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
