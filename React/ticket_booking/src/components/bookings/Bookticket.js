
import React, { useState } from "react";
import axios from "axios";
import {  useNavigate, useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import Navbar from "../Navbar";
import checkAuth from "../auth/checkAuth";


function Booking() {
  const { showId, movieName, showDate, showTime} = useParams();
  const navigate = useNavigate();
  var [numberOfTickets, setNumberOfTickets] = useState(1);
  const user = useSelector((store) => store.auth.user);



  const handleInputChange = (e) => {
    setNumberOfTickets(e.target.value);
  };

  // console.log(user.token)

  function bookTicket() {
    axios
      .post(`http://127.0.0.1:8000/api/book_show/${showId}/`,
      {number_of_tickets:numberOfTickets},{
        headers: {
          Authorization: `Bearer ${user.token}`
        }
          // Added space after "Bearer"
    })
      .then((response) => {
        const booking_id = response.data.id;
        navigate(`/bookshow/confirmation/${booking_id}`);
      })
      .catch((error) => {
        console.error("Error booking ticket:", error);
      });
  }

  return (<>
    <Navbar />
    <div className="text-center">
      <h2>Book Your Tickets</h2>
      <div className="card mx-auto" style={{width: "18rem"}}>
        <div className="card-body">
          <h5 className="card-title">{movieName}</h5>
          <p className="card-text">{showDate}</p>
          <p className="card-text">{showTime}</p>
          <div className="form-group">
            <label htmlFor="exampleFormControlSelect1">Number of Tickets</label>
            <select className="form-control" id="exampleFormControlSelect1" onChange={handleInputChange}>
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
              <option>5</option>
            </select>
          </div>
        </div>
          <button className="card-link btn btn-primary" onClick={bookTicket}>Book</button>
    </div>
  </div>
 </>   
  );
  }

export default checkAuth(Booking);
















// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useSelector } from 'react-redux';
// import { useParams } from 'react-router-dom';
// import { useNavigate } from "react-router-dom"

// const Bookticket = () => {
//   const user = useSelector(store => store.auth.user);
//   const [number_of_tickets, setNumber_of_tickets] = useState(1);  // Set the default value to 5
//   const [bookingSuccess, setBookingSuccess] = useState(false);
//   const { showId } = useParams();
//   var navigate = useNavigate();

//   useEffect(() => {
//     console.log('User:', user);
//   }, [user]);

//   const handleBookTicket = () => {
//     if (!user || !user.token) {
//       console.error('User not authenticated');
//       navigate('/login');
//       return;
//     }

//     axios
//       .post(
//         `http://127.0.0.1:8000/api/book_show/${showId}/`,
//         { number_of_tickets: number_of_tickets },
//         {
//           headers: {
//             Authorization: `Bearer ${user.token}`,
//           },
//         }
//       )
//       .then((response) => {
//         const booking_id = response.data.id;
//         navigate(/bookshow/confirmation/${booking_id});
//       })
//       .catch((error) => {
//         console.error("Error booking ticket:", error);
//       });
//   }




//   return (
//     <div>
//       <h1>Bookticket for Show ID: {showId}</h1>
//       {bookingSuccess ? (
//         <div>
//           <p>Booking successful!</p>
//           {/* Optionally, add a redirect or other actions here */}
//         </div>
//       ) : (
//         <form>
//           <div className="form-group">
//             <label htmlFor="number_of_tickets">Number of Tickets:</label>
//             <select
//               className="form-control"
//               id="number_of_tickets"
//               value={number_of_tickets}
//               onChange={(e) => setNumber_of_tickets(e.target.value)}
//             >
//               <option value={1}>1</option>
//               <option value={2}>2</option>
//               <option value={3}>3</option>
//               <option value={4}>4</option>
//               <option value={5}>5</option>
//             </select>
//           </div>
//           <button
//             type="button"
//             className="btn btn-primary"
//             onClick={handleBookTicket}
//           >
//             Book Ticket
//           </button>
//         </form>
//       )}
//     </div>
//   );
// };

// export default Bookticket;



