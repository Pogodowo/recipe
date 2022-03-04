console.log('nowa receptura js')
//const okejosBox=document.getElementById("okejos")
//okejosBox.innerHTML='Zmieniłem HTML'

const formBoxRec= document.getElementById('form-rec')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const submitBox=document.getElementById('dodajRecSubmit')
function removeElementsByClass(className){
    const elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}


function generowanieFormularzaRecepty (){


           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: 'dodajRecForm/',
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.fields.common
            var slownik=response.fields.slownik

           console.log('elementyForm z gen form',elementyForm)
           if (elementyForm!="ten składnik już został dodany"){
            elementyForm.map(item=>{
            if(Array.isArray(item)){if (item[0]==='producent'){
                console.log('mamy tabelę');
                const div=document.createElement('div')
                div.setAttribute('class','input-field')
                const label=document.createElement('label')
                label.textContent=slownik[item[0]]
                //label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");

                //select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${item[0]}`)
                console.log('idwimpucie',`${item[0]}`)

                div.appendChild(label)
                div.appendChild(select)
                formBoxRec.appendChild(div)

                const optionBox= document.getElementById(`${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = slownik[elem]
                optionBox.appendChild(option)
                })}else{ console.log('tutaj będzie select z imputem');
                {
                console.log('mamy tabelę');
                const div=document.createElement('div')
                div.setAttribute('class','input-field')
                const label=document.createElement('label');
                label.textContent=slownik[item[0]]
                //label.setAttribute('class','elFormDelete');
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown select-field");
                //select.setAttribute('id',"optionId");
                //select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${item[0]}`)
                console.log('idwimpucie',`${item[0]}`)
                div.appendChild(label)
                div.appendChild(select)
                formBoxRec.appendChild(div)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}
                }
            }else{

            if (['aa','aa_ad','dodaj_wode','ad'].includes(item)){

            const label=document.createElement('label')
            label.textContent=item
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            check.setAttribute('value','off')
            check.setAttribute('id',`${item}`)
            console.log('idwimpucie',`${item}`)
//            check.setAttribute('class','elFormDelete')
//            label.setAttribute('class','elFormDelete')
            //check.setAttribute('class','checkBox')
            check.setAttribute('name','checkBox')
            formBoxRec.appendChild(check)
            formBoxRec.appendChild(label)
            console.log('checkvalue',check.value)
            } else
            {
            const div=document.createElement('div')
            div.setAttribute('class','input-field')
            const label=document.createElement('label')
            label.textContent=slownik[item]
            const input=document.createElement('input')
//            input.setAttribute('class','elFormDelete')
//            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${item}`)
            console.log('idwimpucie',`${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')

            div.appendChild(label)
            div.appendChild(input)
            formBoxRec.appendChild(div)
            formBoxRec.appendChild(br)
            }}
            })



            }else{const label=document.createElement('label')
            label.textContent='Ten składnik został już dodany. Czy chcesz go edytować? '
//            label.setAttribute('class','elFormDelete')
            formBoxRec.appendChild(label)
            }
//////////////////////////generoeanir fomularza do czopków/////////////////////////////////
          var rodzajBox = document.getElementById('rodzaj')

        rodzajBox.addEventListener('change',function ()  {removeElementsByClass('elFormDelete');
          var rodzaj=rodzajBox.value
          console.log('rodzaj',rodzaj)
          var szczegForm=response.fields[rodzaj]
          console.log('szczegForm',szczegForm)
          szczegForm.map(item=>{
            if(Array.isArray(item)){if (['czopki_czy_globulk','ilosc_czop_glob','rodzaj',].includes(item)){
                console.log('mamy tabelę');
                const label=document.createElement('label')
                label.textContent=slownik[item[0]]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${item[0]}`)
                console.log('idwimpucie',`${item[0]}`)
                formBoxRec.appendChild(label)
                formBoxRec.appendChild(select)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${item[0]}`)
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
                const div=document.createElement('div')
                div.setAttribute('class','input-field')
                label.textContent=slownik[item[0]]
                label.setAttribute('class','elFormDelete');
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete select-field')
                select.setAttribute('id',`${item[0]}`)
                console.log('idwimpucie',`${item[0]}`)
                div.appendChild(label)
                div.appendChild(select)
                //formBoxRec.appendChild(br)
                formBoxRec.appendChild(div)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = slownik[elem]
                optionBox.appendChild(option)
                })}
                }
            }else{

            if (['aa','aa_ad','dodaj_wode','ad'].includes(item)){
            const label=document.createElement('label')
            label.textContent=item
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            check.setAttribute('value','off')
            check.setAttribute('id',`${item}`)
            console.log('idwimpucie',`${item}`)
            check.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            //check.setAttribute('class','checkBox')
            check.setAttribute('name','checkBox')
            formBoxRec.appendChild(check)
            formBoxRec.appendChild(label)
            console.log('checkvalue',check.value)
            } else
            {
            const div=document.createElement('div')
            div.setAttribute('class','input-field')
            const label=document.createElement('label')
            label.textContent=slownik[item]
            const input=document.createElement('input')
            input.setAttribute('class','elFormDelete input-field')
            input.setAttribute('placeholder',`${slownik[item]}`)
            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${item}`)
            console.log('idwimpucie',`${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')

            div.appendChild(label)
            div.appendChild(input)
            div.appendChild(br)
            formBoxRec.appendChild(div)
            }}
            })
            })




///////////////////////////////////////////////////////////////////////////////////////////////
            },
            error : function (response){
            console.log('error', error)}
            })
            }



function dodawanieSkl(){

                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrf[0].value,}

                var elements = document.getElementById("form-rec").elements;
                console.log('elements',elements)
                for (var i = 0, element; element = elements[i++];) {
                if (element){
                console.log("mamy element");
                dataf[element.id]=element.value;
                 }}

                console.log('dataf',dataf)

                $.ajax({
                type: 'POST' ,
                url:'dodawanieRecJson/',
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');
                         console.log('response.tabela',response.dict)
                         location.href = 'mojerec'

                                        },
                error : function(error){
                         console.log(' dupa nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');



                 }


                    /////tu koniec wstawania//////


generowanieFormularzaRecepty()
submitBox.addEventListener('click', dodawanieSkl)