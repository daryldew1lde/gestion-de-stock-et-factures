$('#printInvoice').click(function(){
    Popup($('.invoice')[0].outerHTML);
    function Popup(data) 
    {
        var fact = document.querySelector("#invoice").innerHTML;
        var body = document.body.innerHTML;
        document.body.innerHTML = fact;
        console.log(document.body.innerHTML);
        window.print();
        document.body.innerHTML = body;
        return true;
    }
});


