

import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import { useSelector } from 'react-redux';
import axios from 'axios';


function Mybookings() {
  const [myBooks, setMybooks] = useState([]);
  const user = useSelector((store) => store.auth.user);


  const headers = user ? { Authorization: `Token ${user.token}` } : {};

  const handleDownload = (bookingId) => {
    // Make a request to the Django API to download the PDF
    axios
      .get(`http://127.0.0.1:8000/api/generate_pdf/${bookingId}`, {
        headers,
        responseType: 'blob', // Set responseType to 'blob' for binary data
      })
      .then((response) => {
        // Create a Blob from the response data
        const blob = new Blob([response.data], { type: 'application/pdf' });

        // Create a link element to trigger the download
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `booking_${bookingId}.pdf`;

        // Append the link to the body and trigger the download
        document.body.appendChild(link);
        link.click();

        // Remove the link from the body
        document.body.removeChild(link);
      })
      .catch((error) => {
        console.error('Error fetching PDF:', error);
      });
  };

  useEffect(() => {
    if (user) {
      // Only fetch bookings if the user is logged in
      axios
        .get('http://127.0.0.1:8000/api/my_bookings/', { headers })
        .then((response) => {
          setMybooks(response.data);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    }
  }, [user, headers]);

  return (
    <>
      <Navbar />
      <br />
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <table className="table table-striped">
              <thead className="thead-dark">
                <tr>
                  <th scope="col">Booking Id</th>
                  <th scope="col">Movie</th>
                  <th scope="col">Show Date</th>
                  <th scope="col">Show Time</th>
                  <th scope="col">Number of Tickets</th>
                  <th scope="col">Ticket</th>
                </tr>
              </thead>
              {myBooks.map((myBook) => (
                <tbody key={myBook.booking_id}>
                  <tr>
                    <th scope="row">{myBook.booking_id}</th>
                    <td>{myBook.movie_name}</td>
                    <td>{myBook.show_date}</td>
                    <td>{myBook.show_time}</td>
                    <td>{myBook.no_of_tickets}</td>
                    <td>
                      <button
                        className="btn btn-success"
                        onClick={() => handleDownload(myBook.id)}>
                        Download
                      </button>
                    </td>
                  </tr>
                </tbody>
              ))}
            </table>
          </div>
        </div>
      </div>
    </>
  );
}

export default Mybookings;