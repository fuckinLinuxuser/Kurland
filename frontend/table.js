console.log("table.js loaeddddddd");
fetch("menu.json")
  .then(res => res.json())
  .then(data => renderMenu(data.categories))
  .catch(err => console.error(err));

function renderMenu(categories) {
  const container = document.getElementById("menu-table");
  container.innerHTML = ""; // очистка

  categories.forEach(cat => {
    const catDiv = document.createElement("div");
    catDiv.className = "category-block";

    // заголовок категории
    const h3 = document.createElement("h3");
    h3.textContent = cat.name;
    catDiv.appendChild(h3);

    // таблица блюд
    const table = document.createElement("table");
    table.className = "menu-table";

    const header = document.createElement("tr");
    header.innerHTML = "<th>Блюдо</th><th>Цена</th>";
    table.appendChild(header);

    cat.items.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.price} ₽</td>
      `;
      table.appendChild(row);
    });

    catDiv.appendChild(table);
    container.appendChild(catDiv);
  });
}              
