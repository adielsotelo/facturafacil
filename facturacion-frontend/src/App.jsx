import UploadBox from './components/UploadBox'

export default function App() {
  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem', textAlign: 'center' }}>
      <img src="/logo.png" alt="Grupo Sachman" style={{ width: 100, marginBottom: 16 }} />
      <h1>FacturaFácil</h1>
      <h2>Grupo Sachman</h2>
      <p>Procesa tu ticket con OCR y recibe instrucciones para facturación</p>
      <UploadBox />
    </div>
  )
}
