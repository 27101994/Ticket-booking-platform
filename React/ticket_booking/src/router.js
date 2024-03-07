

import { createBrowserRouter } from "react-router-dom";

import App from "./App";
import Register from "./components/auth/register";
import Login from "./components/auth/Login"
import Showlist from "./components/bookings/Showlist";
import Bookticket from "./components/bookings/Bookticket";
import Bookconfirmation from "./components/Bookconfirmation";
import Mybooking from "./components/Mybooking";

const router = createBrowserRouter([
    { path: '/', element: <App/> },
    { path: '/login', element: <Login/> },
    { path: '/register', element:<Register/>},
    { path: '/show_list/:movieId', element:<Showlist/>},
    { path: '/book_show/:showId', element:<Bookticket/>},
    {path: '/bookshow/confirmation/:id', element: <Bookconfirmation /> },
    {path: '/my_bookings', element: <Mybooking /> },

]);

export default router;