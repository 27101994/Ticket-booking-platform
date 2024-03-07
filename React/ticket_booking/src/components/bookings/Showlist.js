import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

const Showlist = () => {
    const { movieId } = useParams();
    const [shows, setShows] = useState([]);

    useEffect(() => {
        // Fetch shows for the specific movie ID from the API endpoint
        axios.get(`http://127.0.0.1:8000/api/show_list/${movieId}/`)
            .then(response => {
                setShows(response.data);
            })
            .catch(error => {
                console.error('Error fetching shows:', error);
            });
    }, [movieId]); // Include movieId in the dependency array to re-fetch shows when it changes

    return (
        <div className="container mt-5">
            <h1 className="mb-4">Showlist for Movie ID: {movieId}</h1>
            <div>
                {shows.map(show => (
                    <div key={show.id} className="card mb-4">
                        <div className="card-body">
                            <h2 className="card-title">{show.movie.title}</h2>
                            <p className="card-text">Show Time: {show.show_time}</p>
                            <p className="card-text">Date: {show.date}</p>
                            <p className="card-text">Is Disabled: {show.is_disabled ? 'Yes' : 'No'}</p>
                            <p className="card-text">Ticket Price: {show.ticket_price}</p>
                            <button className="btn btn-primary">
                                <Link to={`/book_show/${show.id}`} className="text-white">
                                    <button className="btn btn-primary">Book Ticket</button>
                                </Link>
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Showlist;
