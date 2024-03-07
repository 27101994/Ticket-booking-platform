
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import Navbar from "./Navbar";
import checkAuth from "./auth/checkAuth";

function Bookconfirmation() {
  const { id } = useParams();
  const [bookconfirm, setBookconfirm] = useState({});
  const user = useSelector((store) => store.auth.user);
  const headers = {
    Authorization: `Token ${user.token}`,
  };

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/book_my_movies_api/booking/confirmation/${id}`, { headers })
      .then((response) => {
        setBookconfirm(response.data);
      })
      .catch((error) => {
        console.error("Error fetching confirmation:", error);
      });
  },[id]);

  return (
    <>
    <Navbar />
      {bookconfirm && (
        <div className="text-center">
            <h1>Dear {bookconfirm.username} thanks for your Booking</h1>
            <h4>Your ticket is confirmed</h4>
            <div className="card mx-auto mb-3" style={{width:'400px'}}>
                <div className="card-body">
                    <h5 className="card-title">{bookconfirm.movie_name}</h5>
                    <p className="card-text">Booking ID: {bookconfirm.booking_id}</p>
                    <p className="card-text">Show Date: {bookconfirm.show_date}</p>
                    <p className="card-text">Show Time: {bookconfirm.show_time}</p>
                    <p className="card-text">Number of Tickets: {bookconfirm.no_of_tickets}</p>
                </div>
            </div>
        </div>
      )}
    </>
  );
}

export default checkAuth(Bookconfirmation);