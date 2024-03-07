import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../Navbar";

function Register() {
    var [username, setUsername] = useState('');
    var [password1, setPassword1] = useState('');
    var [password2, setPassword2] = useState('');
    var [errorMessage, setErrorMessage] = useState('');
    var navigate = useNavigate();

    function registerUser() {
        var user = {
            username: username,
            password1: password1,
            password2: password2
        };

        axios.post('http://127.0.0.1:8000/api/signup/', user)
            .then(response => {
                setErrorMessage('');
                navigate('/');
            })
            .catch(error => {
                if (error.response.data.username) {
                    setErrorMessage(error.response.data.username[0]);
                } else if (error.response.data.password1) {
                    setErrorMessage(error.response.data.password1[0]);
                } else if (error.response.data.password2) {
                    setErrorMessage(error.response.data.password2[0]);
                } else {
                    setErrorMessage('Failed to connect to the API');
                }
            });
    }

    return (
        <div>
            <Navbar />
            <div className="container">
                <div className="row">
                    <div className="col-8 offset-2">
                        <h1>Register</h1>
                        {errorMessage ? <div className="alert alert-danger">{errorMessage}</div> : ''}
                        <div className="form-group">
                            <label>Username:</label>
                            <input
                                type="text"
                                className="form-control"
                                value={username}
                                onChange={(event) => setUsername(event.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Password:</label>
                            <input
                                type="password"
                                className="form-control"
                                value={password1}
                                onChange={(event) => setPassword1(event.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Confirm Password:</label>
                            <input
                                type="password"
                                className="form-control"
                                value={password2}
                                onChange={(event) => setPassword2(event.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <button className="btn btn-primary float-right" onClick={registerUser}>Submit</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Register;
