import { useState } from 'react'

export default function UploadBox() {
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  const handleFile = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('ticket', file)

    setLoading(true)
    setResult('')

    try {
      const res = await fetch('https://TU_BACKEND_URL/api/process-ticket', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      setResult(data.text)
    } catch (e) {
      setResult('❌ Error al procesar el ticket')
    }

    setLoading(false)
  }

  return (
    <div style={{ marginTop: '2rem' }}>
      <input type="file" accept="image/*" onChange={handleFile} />
      {loading && <p>⏳ Procesando...</p>}
      {result && (
        <div style={{ marginTop: '1rem', background: '#fff', padding: '1rem', borderRadius: '6px', boxShadow: '0 0 10px #ccc' }}>
          <strong>🧾 Resultado OCR:</strong>
          <pre style={{ textAlign: 'left' }}>{result}</pre>
        </div>
      )}
    </div>
  )
}
