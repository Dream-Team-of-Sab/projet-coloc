let btn = document.getElementsByClassName("see");
for (i = 0; i < btn.length; ++i) {
    btn[i].addEventListener('click', (event) => {
        event.preventDefault();
        const id = event.path[0].dataset.id;
        const invoice = document.getElementById('result')
        fetch(`http://0.0.0.0/invoice/${id}`).then((response) => {
            response.json().then(json => {
                let title = cE('p');
                title.append("Facture : ", json.title);
                let date = cE('p');
                date.append("Ajoutée le : ", json.date);
                let price = cE('p');
                price.append("Montant total : ", json.price, "€");
                let details = cE('p');
                details.append("Détail de la facture : ", json.details);
                document.getElementById('invoice_img').src=`/static/uploads/${json.file_name}`
                invoice.append(title, date, price, details)
                document.getElementById('big_invoice').href= `/static/uploads/${json.file_name}` 
            })
        })
    })
}    

// Pour vider le modal
$('#seeInvoice').on('hidden.bs.modal', function (e) {
    $('#seeInvoice').find('.modal-body')[0].innerHTML = ""
})

function cE(type) {
    return document.createElement(type)
}
