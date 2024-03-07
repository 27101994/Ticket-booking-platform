import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Fetch movies from the API endpoint
    axios.get('http://127.0.0.1:8000/api/movie_list/')
      .then(response => {
        setMovies(response.data);
      })
      .catch(error => {
        console.error('Error fetching movies:', error);
      });
  }, []); // Empty dependency array means this effect will run once when the component mounts
      console.log(movies)
  return (
    <div>
      <Navbar />

      <div className="App container-fluid">
        <h1 className="mt-4 mb-4">Movie List</h1>
        <div className="row">
          {movies.map(movie => (
            <div key={movie.id} className="col-md-4 mb-4">
              {/* Wrap the card in a Link component */}
              <Link to={`/show_list/${movie.id}`} className="card-link">
                <div className="card">
                  {/* Use the correct base URL for images */}
                  <img src={`http://127.0.0.1:8000${movie.image}`} alt={movie.title} className="card-img-top img-fluid" style={{objectFit:'cover',height:'550px'}} />
                  <div className="card-body">
                    <h5 className="card-title">{movie.title}</h5>
                    {/* Display other movie details as needed */}
                  </div> 
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
