console.log('O co tu chodzi?')
console.log('dupa?')
const modalBox=document.getElementById("exampleModal")
//const skladnikBox= document.getElementById('wybieraj');
const modalTytul=document.getElementById("exampleModalLabel")
const formBox= document.getElementById('modal-form')
const closeButton=document.getElementById('close-button')
const dodajSkladnikButton=document.getElementById("dodajsklbutton")
const prowizorycznatabelaBox=document.getElementById('prowizorycznatabela')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const tabelaDocelowa=document.getElementById('tabela-docelowa')
//console.log('tabelaDocelowa',tabelaDocelowa)
const deleteButtons=document.getElementsByClassName("btn-close")
const inputBox=document.getElementById("myInput")
const autocompleteButton=document.getElementById("submitButton")
cardBox=document.getElementById('cards')
console.log('close buttons', deleteButtons)
const mojeRecBox=document.getElementById("tabela-moje-rec")
const idBox=document.getElementById("pk-box")
console.log('id-box',idBox)
const sklId=idBox.innerText
console.log('sklId',sklId)
const elementyForm={}




var ingridients=["witamina A","witamina E","Hydrokortyzon","Metronidazol","Wazelina","Mocznik","Woda destylowana"]
/////////////////js do autouzupełniania////////////////////////////////////////////////////////////
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}


autocomplete(inputBox, ingridients);
////koniec js do autouzupełmiania/////////////////////////////////////////////////////////////////


/////funkcja do usuwania składnika///////////////////////////

function usuwanieSkladnika (pk){
        $.ajax({
                        type: 'GET',
                        url: `delSkl/${ pk }/`,
                        success : function(response){console.log('sukces ajaxa z del');
                        cardBox.innerHTML=''
                        tabelaDocelowa.innerHTML='';
                        updateTable()

                        },//koniec sukcesa
                        error : function (error){console.log('brak sukcesu ajaxa z del')},
                        })

}

//function listaElemForm(){
//            skl=inputBox.value;
//            $.ajax({
//            type: 'GET',
//            url: `formJson/${ skl }/`,
//            success : function(response){
//            console.log('succes spobrania do forma', response);
//            var elementyForm = response.datadict
//            console.log('wczesne elementy form',elementyForm)
//
//            },
//            error : function (response){
//            console.log('error', error)}
//            })
//            }


function generowanieFormularza (){
          skl=inputBox.value;
          console.log('skladnik',skl);
          modalTytul.innerText=inputBox.value;
           $("#exampleModal").modal('show');
           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: `formJson/${ skl }/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.datadict
           console.log('elementyForm z gen form',elementyForm)
            elementyForm.map(item=>{
            if(Array.isArray(item)){if (item[0]==='producent'){
                console.log('mamy tabelę');
                const label=document.createElement('label')
                label.textContent=item[0]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}else{ console.log('tutaj będzie select z imputem');
                {
                console.log('mamy tabelę');
                const label=document.createElement('label');
                label.textContent=item[0]
                label.setAttribute('class','elFormDelete');
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                formBox.appendChild(br)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}
                }
            }else{

            if (['aa','aa_ad','dodaj wodę'].includes(item)){
            const label=document.createElement('label')
            label.textContent=item
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            check.setAttribute('value','off')
            check.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            check.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            //check.setAttribute('class','checkBox')
            check.setAttribute('name','checkBox')
            formBox.appendChild(check)
            formBox.appendChild(label)
            console.log('checkvalue',check.value)
            } else
            {
            const label=document.createElement('label')
            const input=document.createElement('input')
            input.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            label.textContent=item
            formBox.appendChild(label)
            formBox.appendChild(input)
            formBox.appendChild(br)
            }}
            })

            },
            error : function (response){
            console.log('error', error)}
            })
            }




function dodawanieSkl(){
            skl=inputBox.value;
            $.ajax({
            type: 'GET',
            url: `formJson/${ skl }/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.datadict
            console.log('wczesne elementy form',elementyForm)

                const checkButtons = document.getElementsByName('checkBox')
                console.log('checkButtons',checkButtons)
                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
                /////////////////////////////////////////////////////////////////////////////
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrf[0].value,'skladnik':skl,'receptura_id':sklId}
                console.log('elementyForm1',elementyForm)
                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){ console.log('na razie nie umiem tabeli',
                `${skl}-${elementyForm[i][0]}`);
                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
                else
                {console.log('i',i,`${skl}-${elementyForm[i]}`);
                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}
                console.log('elementyForm2',elementyForm)
                console.log('dataf',dataf)

                $.ajax({
                type: 'POST' ,
                url:`dodajskl/${sklId}/`,
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');
                         console.log('response.tabela',response.tabela)
                         tabelaDocelowa.innerHTML=''
                         updateTable()
                                        },
                error : function(error){
                         console.log(' dupa nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');
                 $("#exampleModal").modal('hide');


                 },
            error : function (response){
            console.log('error', error)}
            })
            }

                    /////tu koniec wstawania//////





////////////////////////////////////////////////////////////
////////funkcja z ajaxem do aktualizacji taveli///////
function updateTable(){
         $.ajax({
            type: 'GET',
            url:`aktualizujTabela/${sklId}/`,
            success : function(response){
            console.log('Sukces ajaxa z tabelą', response);
            let elementyTabeli=response.tabela_zbiorcza
            console.log('elementyTabeli', response.tabela_zbiorcza)

            //let tabelaDocelowa=document.getElementById("tabela-docelowa");
            tabelaDocelowa.innerHTML='';
            cardBox.innerHTML=''
            var numElem=1
            elementyTabeli.map(item=>{
            console.log('itemTabeli',item.fields.skladnik);
            const div=document.createElement('div')
            ///////dodawanie przycisku do usuwania////////////////
            var deleteButton = document.createElement("button");

//          element.type = type;type="button" class="close" data-dismiss="modal" aria-label="Close"
            deleteButton.setAttribute('type','button');
            deleteButton.setAttribute('class',"btn-close");
            deleteButton.setAttribute('aria-label','Close');
            deleteButton.setAttribute('id',item.pk);
            //deleteButton.setAttribute('onclick',delItem);
            deleteButton.onclick = function() {usuwanieSkladnika(item.pk);
            }



            //////////////////////////////////////////////////////
            if (item.fields.show===true){
            div.innerHTML+= numElem+') ' + item.fields.skladnik+'  '
            if (item.fields.aa==='on'){div.innerHTML+='aa '}
            else if(item.fields.aa_ad==='on'){div.innerHTML+='aa ad '}
            if (item.fields.ilosc_na_recepcie!=='') {div.innerHTML+=+item.fields.ilosc_na_recepcie}
            console.log('div',div);
            div.appendChild(deleteButton);
            tabelaDocelowa.appendChild(div);
            }


            //div.innerHTML+='<br>'
            ///////////////dodawanie kart/////////////////
      card=document.createElement('div')

          card.setAttribute('class','card')
          card.setAttribute('style','width: 36rem;')

   var ul=document.createElement('ul')
        ul.setAttribute('class','list-group list-group-flush')
   var li=document.createElement('li')
        li.setAttribute('class','list-group-item')
        li.innerHTML=numElem+')   '+item.fields.skladnik
        ul.appendChild(li)
   var li2=document.createElement('li')
       //li2.classList.add( 'li-inline');
       li2.setAttribute('class','list-group-item')
       //li2.setAttribute('class','li-inline')

        /////////wypisywanie atrybutów danego składnika/////
        for (const [key, value] of Object.entries(item.fields)){ if ( value!=null && value!='0'){
//                                                          const div=document.createElement('div')
                  li2.innerHTML+=' '+key+': '
                  li2.innerHTML+=value+' ,'
//                                                          prowizorycznatabelaBox.appendChild(div)
                                                    }}
        ///////////////////////////////////////////////////

        ul.appendChild(li2)
        card.appendChild(ul)
        cardBox.appendChild(card)
        numElem+=1



            //////////////////////////////////////////////


            })
            },
            error : function (error){console.log('error')},
            })
}
//////////koniec funkcji z ajaxem do aktualizacji tabeli//////
////funkcja do usuwania formularza z modala
function removeElementsByClass(className){
    const elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}
////////////////////////////////////////////////////////////////////
const dodanyId=0

updateTable()





/////////////////////////////////////////////////////////////////////////////////////////////
//autocompleteButton.addEventListener( 'click', e=>{console.log('kliknąłem autocomplete button');
//          skl=inputBox.value;
//          console.log('skladnik',skl);
//          modalTytul.innerText=inputBox.value;
//           $("#exampleModal").modal('show');
//           ////////////////ajax pobieranie elementów formularza///////////////////////////////
//           $.ajax({
//            type: 'GET',
//            url: `formJson/${ skl }/`,
//            success : function(response){
//            console.log('succes spobrania do forma', response);
//            var elementyForm = response.datadict
//            console.log('wczesne elementy form',elementyForm)
//
//            elementyForm.map(item=>{
//            if(Array.isArray(item)){if (item[0]==='producent'){
//                console.log('mamy tabelę');
//                const label=document.createElement('label')
//                label.textContent=item[0]
//                label.setAttribute('class','elFormDelete');
//                const select=document.createElement('select');
//                select.setAttribute('class',"ui dropdown");
//                //select.setAttribute('id',"optionId");
//                select.setAttribute('class','elFormDelete')
//                select.setAttribute('id',`${skl}-${item[0]}`)
//                console.log('idwimpucie',`${skl}-${item[0]}`)
//                formBox.appendChild(label)
//                formBox.appendChild(select)
//                //const optionBox= document.getElementById('optionId')
//                const optionBox= document.getElementById(`${skl}-${item[0]}`)
//                const slicedArray=item.slice(1)
//                console.log(item[0])
//                slicedArray.map(elem=>{
//                const option=document.createElement('option')
//                option.textContent = elem
//                optionBox.appendChild(option)
//                })}else{ console.log('tutaj będzie select z imputem');
//                {
//                console.log('mamy tabelę');
//                const label=document.createElement('label');
//                label.textContent=item[0]
//                label.setAttribute('class','elFormDelete');
//                const br=document.createElement('br')
//                br.setAttribute('class','elFormDelete')
//                const select=document.createElement('select');
//                select.setAttribute('class',"ui dropdown");
//                //select.setAttribute('id',"optionId");
//                select.setAttribute('class','elFormDelete')
//                select.setAttribute('id',`${skl}-${item[0]}`)
//                console.log('idwimpucie',`${skl}-${item[0]}`)
//                formBox.appendChild(label)
//                formBox.appendChild(select)
//                formBox.appendChild(br)
//                //const optionBox= document.getElementById('optionId')
//                const optionBox= document.getElementById(`${skl}-${item[0]}`)
//                const slicedArray=item.slice(1)
//                console.log(item[0])
//                slicedArray.map(elem=>{
//                const option=document.createElement('option')
//                option.textContent = elem
//                optionBox.appendChild(option)
//                })}
//                }
//            }else{
//
//            if (item=='aa' || item=='aa_ad'){
//            const label=document.createElement('label')
//            label.textContent=item
//            const check = document.createElement("input");
//            check.setAttribute('type',"checkbox")
//            check.setAttribute('value','off')
//            check.setAttribute('id',`${skl}-${item}`)
//            console.log('idwimpucie',`${skl}-${item}`)
//            check.setAttribute('class','elFormDelete')
//            label.setAttribute('class','elFormDelete')
//            //check.setAttribute('class','checkBox')
//            check.setAttribute('name','checkBox')
//            formBox.appendChild(check)
//            formBox.appendChild(label)
//            console.log('checkvalue',check.value)
//            } else
//            {
//            const label=document.createElement('label')
//            const input=document.createElement('input')
//            input.setAttribute('class','elFormDelete')
//            label.setAttribute('class','elFormDelete')
//            input.setAttribute('id',`${skl}-${item}`)
//            console.log('idwimpucie',`${skl}-${item}`)
//            const br=document.createElement('br')
//            br.setAttribute('class','elFormDelete')
//            label.textContent=item
//            formBox.appendChild(label)
//            formBox.appendChild(input)
//            formBox.appendChild(br)
//            }}
//            })
//
//
//            dodajSkladnikButton.addEventListener('click',e=>{console.log('kliknąłem dodaj składnik');
//                /////tutaj wstawię kod który będzie sprawdzał czy radio button jest wciśnięty///
//                const checkButtons = document.getElementsByName('checkBox')
//                console.log('checkButtons',checkButtons)
//                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
//                /////////////////////////////////////////////////////////////////////////////
//                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
//                dataf={'csrfmiddlewaretoken': csrf[0].value,'skladnik':skl,'receptura_id':sklId}
//                console.log('elementyForm1',elementyForm)
//                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){ console.log('na razie nie umiem tabeli',
//                `${skl}-${elementyForm[i][0]}`);
//                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
//                else
//                {console.log('i',i,`${skl}-${elementyForm[i]}`);
//                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}
//                console.log('elementyForm2',elementyForm)
//                console.log('dataf',dataf)
//
//                $.ajax({
//                type: 'POST' ,
//                url:`dodajskl/${sklId}/`,
//                data : dataf,
//                success: function(response){
//                         console.log('wygrywamy');
//                         console.log('response.tabela',response.tabela)
//                         tabelaDocelowa.innerHTML=''
//                         updateTable()
//                                        },
//                error : function(error){
//                         console.log(' dupa nie działa');
//                                                    }
//                 });
//                 /////koniec ajaxa
//                 removeElementsByClass('elFormDelete');
//                 $("#exampleModal").modal('hide');
//                 })
//                    /////tu koniec wstawania//////
//                    },
//            error : function (response){
//            console.log('error', error)}
//            })
//         })

//////////////////////3pozycja/////////////////////////////////////////////////////
autocompleteButton.addEventListener( 'click',generowanieFormularza );
dodajSkladnikButton.addEventListener('click',dodawanieSkl );
closeButton.addEventListener('click',e=>{console.log('kliknąłem close ');$("#exampleModal").modal('hide');
                                           removeElementsByClass('elFormDelete'); })




////////////////////////////////////////////////////////////////////////////////////////////////












