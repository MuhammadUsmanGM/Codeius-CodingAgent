import './App.css'
import Navbar from './components/Navbar'
import InputField from './components/InputField'

function App() {
  return (
    <div className="App">
      <Navbar />
      {/* The background image remains visible as the background of the App div */}
      <div className="input-section">
        <InputField />
      </div>
    </div>
  )
}

export default App
