// Простая реализация: Express + file-based storage
const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const PORT = process.env.PORT || 8082;
const ADMIN_USER = process.env.ADMIN_USER || 'admin';
const ADMIN_PASS = process.env.ADMIN_PASS || 'changeme';
const DATA_FILE = path.join(__dirname, 'menu.json');

const app = express();
app.use(cors()); // разрешаем публичному сайту делать fetch
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // админ UI

// --- Простая basic auth middleware для защиты админ UI и POST
function basicAuth(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth) return unauthorized(res);
  const match = auth.match(/^Basic (.+)$/);
  if (!match) return unauthorized(res);
  const cred = Buffer.from(match[1], 'base64').toString();
  const [user, pass] = cred.split(':');
  if (user === ADMIN_USER && pass === ADMIN_PASS) return next();
  return unauthorized(res);
}
function unauthorized(res) {
  res.set('WWW-Authenticate', 'Basic realm="Admin Area"');
  return res.status(401).send({ error: 'Unauthorized' });
}

// --- Utility: read/write menu file
function readMenu() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // fallback: пустая структура
    return { last_updated: new Date().toISOString(), currency: 'RUB', categories: [] };
  }
}
function writeMenu(obj) {
  fs.mkdirSync(path.dirname(DATA_FILE), { recursive: true });
  // атомарная запись: tmp -> rename
  const tmp = DATA_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(obj, null, 2), 'utf8');
  fs.renameSync(tmp, DATA_FILE);
}

// --- Public API: возвращает меню (все позиции)
app.get('/api/menu', (req, res) => {
  const menu = readMenu();
  res.json(menu);
});

// --- Admin-only: обновление availability или замена всего меню
// Ожидается body:
// { updates: [{ id: 'g1', available: true }, ...], editor: 'Имя' }
// или можно передать { menu: { ... } } для замены целиком
app.post('/api/update', basicAuth, (req, res) => {
  try {
    const payload = req.body || {};
    const menu = readMenu();

    if (payload.menu) {
      // Полная замена (админ может загрузить новый полный JSON)
      payload.menu.last_updated = new Date().toISOString();
      writeMenu(payload.menu);
      return res.json({ ok: true, message: 'Menu replaced' });
    }

    const updates = payload.updates || [];
    if (!Array.isArray(updates)) return res.status(400).json({ ok: false, error: 'updates must be array' });

    // Проходим по категориям и позициям, применяем updates по id
    const idToItem = {};
    menu.categories.forEach(cat => {
      (cat.items || []).forEach(it => {
        idToItem[it.id] = it;
      });
    });

    updates.forEach(u => {
      if (u && u.id && idToItem[u.id]) {
        idToItem[u.id].available = !!u.available;
        if (u.price !== undefined) idToItem[u.id].price = Number(u.price) || idToItem[u.id].price;
      }
    });

    menu.last_updated = new Date().toISOString();
    writeMenu(menu);
    return res.json({ ok: true, last_updated: menu.last_updated });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ ok: false, error: String(err) });
  }
});

// --- Serve admin UI (index.html in public) protected by auth
app.get('/', basicAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

// --- Start
app.listen(PORT, () => {
  console.log(`Admin server listening on http://0.0.0.0:${PORT}`);
});