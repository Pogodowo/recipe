const listaSkladnikowDrop=document.getElementById("lista-dropdown" )
var ingridients=['3% roztwór kwas borowy', 'Anestezyna', 'Balsam Peruwiański', 'Bizmutu azotan zasadowy',
'Bizmutu węglan zasadowy', 'Detreomycyna', 'Efedryna', 'Erytromycna', 'Etanol', 'Euceryna', 'Gliceryna 86%',
'Hascobaza', 'Hydrokortyzon', 'Ichtiol', 'Lanolina', 'Maść Cholesterolowa', 'Metronidazol', 'Mocznik', 'Neomycyna',
'Nystatyna', 'Oleum Cacao', 'Oleum Menthae piperitae',
'Prokaina', 'Rezorcyna', 'Witamina A', 'Wazelina biała', 'Wazelina żółta', 'Woda destylowana', 'witamina E','Tlenek Cynku','Olej Rycynowy','Papaweryna','Mentol','Laktoza','Kwas Salicylowy']
function myFunction(){}

function listaSkladnikowDropFunc(){
          const ul=document.createElement('ul')
          ul.setAttribute('class','column-dropdown')
          ingridients.map(item=>{
          const p=document.createElement('p')
          p.setAttribute('class','drop-ingridient-item')
          const a=document.createElement('a')
          a.setAttribute('class',"dropdown-item");
          a.setAttribute('onclick',`if(getElementById('myInput')!=null){getElementById('myInput').value = '${item}'}else{myFunction()}`);
          a.innerText=item
          p.appendChild(a)
          ul.appendChild(p)
          })
          listaSkladnikowDrop.appendChild(ul)
          }



//function listaSkladnikowDropFunc(){
//        var perChunk = 7 // items per chunk
//        var result = ingridients.reduce((resultArray, item, index) => {
//         const chunkIndex = Math.floor(index/perChunk)
//        if(!resultArray[chunkIndex]) {
//        resultArray[chunkIndex] = [] // start a new chunk
//            }
//          resultArray[chunkIndex].push(item)
//        return resultArray
//        }, [])
//
//          for (let i = 0; i < result.length; i++) {
//
//          const ul=document.createElement('ul')
//
//          result[i].map(item=>{
//          const p=document.createElement('p')
//          const a=document.createElement('a')
//          a.setAttribute('class',"dropdown-item");
//          a.setAttribute('onclick',`if(getElementById('myInput')!=null){getElementById('myInput').value = '${item}'}else{myFunction()}`);
//          a.innerText=item
//          p.appendChild(a)
//          ul.appendChild(p)
//
//
//          })
//          listaSkladnikowDrop.appendChild(ul)
//          }
//
//
//          }
//


 listaSkladnikowDropFunc()