function changeHeader (color){
    document.getElementById('header').style.backgroundColor=color;
}   

function changeListHead (color){
    document.getElementById('kate').style.backgroundColor=color;
}   

function changeList (color){
    var x=document.getElementsByClassName('el');
    for(var i=0;i<x.length;i++){
        x[i].style.backgroundColor=color;
    }      
}   