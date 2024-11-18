let denemeler = [];

function addDeneme() {
    const denemeAdi = document.getElementById("denemeAdi").value;
    const tarih = document.getElementById("tarih").value;
    const dogruSayisi = parseInt(document.getElementById("dogruSayisi").value);
    const yanlisSayisi = parseInt(document.getElementById("yanlisSayisi").value);

    if (!denemeAdi || !tarih || isNaN(dogruSayisi) || isNaN(yanlisSayisi)) {
        alert("Lütfen tüm alanları doldurun!");
        return;
    }

    const net = dogruSayisi - (yanlisSayisi * 0.25);
    const successRate = ((dogruSayisi / (dogruSayisi + yanlisSayisi)) * 100).toFixed(2);

    denemeler.push({ denemeAdi, tarih, net: net.toFixed(2), successRate });

    updateTable();
    clearForm();
}

function updateTable() {
    const tbody = document.querySelector("#denemeListesi tbody");
    tbody.innerHTML = "";

    denemeler.forEach((deneme, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${deneme.denemeAdi}</td>
            <td>${deneme.tarih}</td>
            <td>${deneme.net}</td>
            <td>${deneme.successRate}%</td>
        `;
        tbody.appendChild(row);
    });
}

function clearForm() {
    document.getElementById("denemeAdi").value = "";
    document.getElementById("tarih").value = "";
    document.getElementById("dogruSayisi").value = "";
    document.getElementById("yanlisSayisi").value = "";
}
