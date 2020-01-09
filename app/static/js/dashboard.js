let dataDiv = document.getElementById("flatData");
let table = document.createElement('table');
let id = dataDiv.dataset.id;


let bodyWrapper = document.createElement('tbody');
let headWrapper = document.createElement('thead');
let headRaw = document.createElement('tr');
let headName = document.createElement('th');
let headBalance = document.createElement('th');

headBalance.append("Balance");
headName.append("Name");


headRaw.append(headName, headBalance);
headWrapper.append(headRaw);

let btn = document.getElementById("dashboard");
btn.addEventListener('click', (event) => {
    event.preventDefault();
    fetch(`http://0.0.0.0/get_data/${id}`).then((data) => {
        data.json().then((json) => {
            console.log(json)
            bodyWrapper.innerHTML = "";
            for (j of json) {
                console.log(j)
               let tr = document.createElement('tr');
               let name = document.createElement('td');
               let balance = document.createElement('td');
               name.append(j.name)
               balance.append(j.balance)
               tr.append(name, balance)
               bodyWrapper.append(tr);
            } 
            table.append(headWrapper, bodyWrapper);
            table.className = "table table-striped"
            dataDiv.innerHTML = "";
            dataDiv.append(table);
        });
    });
});
// Pour vider le modal
$('#seeInvoice').on('hidden.bs.modal', function (e) {
    $('#seeInvoice').find('.modal-body')[0].innerHTML = ""
})
