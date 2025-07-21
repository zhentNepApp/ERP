const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");
const app = express();
const PORT = 3000;

// Ruta al archivo .db local
const dbPath = path.join(__dirname, "db.db"); // cambia el nombre si el tuyo es diferente
const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
  if (err) console.error("Error al abrir la base de datos:", err.message);
  else console.log("📦 Base de datos SQLite conectada.");
});

// Middleware
app.use(express.static(path.join(__dirname, "public"))); // Carpeta que contiene HTML, CSS y JS
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Endpoint para consulta de terceros
app.post("/buscar-tercero", (req, res) => {
  const { nombreCompleto, nit } = req.body;

  const query = `
    SELECT * FROM terceros
    WHERE "Nombre Completo" = ? AND NIT = ?
  `;

  db.get(query, [nombreCompleto, nit], (err, row) => {
    if (err) {
      console.error("❌ Error SQL:", err.message);
      return res.status(500).json({ error: "Error en la consulta" });
    }
    if (!row) return res.status(404).json({ message: "Tercero no encontrado" });
    res.json(row);
  });
});

// Arrancar servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});
