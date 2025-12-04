import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [status, setStatus] = useState('Checking backend...')
  const [items, setItems] = useState([])

  useEffect(() => {
    // 1. Verify Backend Connection
    axios.get('http://localhost:8000/health')
      .then(res => setStatus(res.data.message))
      .catch(err => setStatus('Backend Disconnected'))
      
    // 2. Fetch Example Data
    axios.get('http://localhost:8000/items')
      .then(res => setItems(res.data))
  }, [])

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">PostCo Tech Test</h1>
      
      {/* Status Badge */}
      <div className={`inline-block px-3 py-1 rounded-full text-white mb-6 ${status.includes('ready') ? 'bg-green-500' : 'bg-red-500'}`}>
        {status}
      </div>

      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Items</h2>
        {items.length === 0 ? <p>No items found.</p> : (
          <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>
        )}
      </div>
    </div>
  )
}

export default App

