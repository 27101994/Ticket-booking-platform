import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { NavLink, useNavigate } from "react-router-dom";
import { removeUser } from "../store/authSlice";

function Navbar() {
    var user = useSelector(store => store.auth.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();


    function logout(){
        if(user){
            axios.post('http://127.0.0.1:8000/api/logout/',{},{
               headers:{'Authorization':"Bearer "+ user.token}
            });
            dispatch(removeUser());
            navigate('/login');
        }
    }
    

    return (
        <nav className="navbar navbar-expand-sm navbar-dark bg-dark">
            <div className="navbar-brand">
                <h4>Book My Show</h4>
            </div>
            <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse mr-auto" id="navbarNav" style={{ float: "left" }}>
                <ul className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <NavLink
                            to={"/"}
                            className="nav-link"
                            activeClassName="active"
                        >
                            Movies
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink
                            to={"/register"}
                            className="nav-link"
                            activeClassName="active"
                        >
                            Register
                        </NavLink>
                    </li>
                    {user ? (<>

                        <li className="nav-item">
                            <NavLink className="nav-link" to='/my_bookings'>
                                My bookings
                            </NavLink>
                        </li>

                        <li className="nav-item">
                            <NavLink className="nav-link" onClick={logout}>
                                Logout
                            </NavLink>
                        </li>
                    </>) : (
                        <li className="nav-item">
                            <NavLink
                                to={"/login"}
                                className="nav-link"
                                activeClassName="active"
                            >
                                Login
                            </NavLink>
                        </li>
                    )}
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
