import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <button onClick={spotify}>Spotify Album</button>
        <button onClick={revoke}>Turn Off</button>
      </header>
    </div>
  );
}

function spotify() {
  alert('Starting spotify');
  fetch('http://localhost:5000/spotify', { method: 'GET' })
    .then((response) => {
      if(!response.ok) throw new Error(response.status);
      else console.log("Spotify call success")
    })
}

function revoke() {
  alert('Turning off');
  fetch('http://localhost:5000/revoke', { method: 'GET' })
    .then((response) => {
      if(!response.ok) throw new Error(response.status);
      else console.log("revoke success")
    })
}

export default App;
